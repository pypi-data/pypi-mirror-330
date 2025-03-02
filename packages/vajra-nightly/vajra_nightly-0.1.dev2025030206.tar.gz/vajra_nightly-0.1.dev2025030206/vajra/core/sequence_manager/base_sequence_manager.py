from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from vajra.config import LLMReplicaControllerConfig
from vajra.datatypes import SamplerOutput  # type: ignore
from vajra.datatypes import SamplerOutputs  # type: ignore
from vajra.datatypes import SequenceStatus  # type: ignore
from vajra.datatypes import (
    RequestOutput,
    SchedulerOutput,
    Sequence,
    SequenceScheduleMetadata,
)
from vajra.utils.threading_utils import synchronized


class BaseSequenceManager(ABC):

    def __init__(self, config: LLMReplicaControllerConfig):
        self.seq_map: Dict[str, Sequence] = {}
        self.enable_sequence_pipeline_parallel = (
            config.parallel_config.enable_sequence_pipeline_parallel
        )

    @synchronized
    def add_seq(self, seq: Sequence) -> None:
        assert seq.seq_id not in self.seq_map
        self.seq_map[seq.seq_id] = seq

    def get_seq(self, seq_id: str) -> Sequence:
        return self.seq_map[seq_id]

    def _free_seq(self, seq_id: str) -> None:
        assert seq_id in self.seq_map
        del self.seq_map[seq_id]

    def _preempt_seq(self, seq_id: str) -> None:
        assert seq_id in self.seq_map
        seq = self.seq_map[seq_id]
        assert seq.is_executing()
        seq.reset_for_recompute()

    def _pause_seq(self, seq_id: str) -> None:
        assert seq_id in self.seq_map
        seq = self.seq_map[seq_id]
        assert seq.is_running(), f"seq_id: {seq_id}, status: {seq.status}"
        seq.status = SequenceStatus.PAUSED

    def _resume_seq(self, seq_id: str) -> None:
        assert seq_id in self.seq_map
        seq = self.seq_map[seq_id]
        assert (
            seq.is_waiting() or seq.is_paused() or seq.is_waiting_preempted()
        ), f"seq_id: {seq_id}, status: {seq.status}"
        seq.status = SequenceStatus.RUNNING

    def _on_seq_scheduled(self, seq_sched_metadata: SequenceScheduleMetadata) -> None:
        assert seq_sched_metadata.seq_id in self.seq_map
        self._resume_seq(seq_sched_metadata.seq_id)

    @abstractmethod
    def _get_block_table(self, seq: Sequence) -> List[int]:
        pass

    @synchronized
    def on_schedule(
        self,
        scheduler_output: SchedulerOutput,
    ) -> Tuple[List[Sequence], List[Sequence]]:
        ignored_seqs: List[Sequence] = []
        for seq_id in scheduler_output.ignored_seq_ids:
            assert seq_id in self.seq_map
            seq = self.seq_map[seq_id]
            ignored_seqs.append(seq)
            self._free_seq(seq_id)

        for seq_id in scheduler_output.preempted_seq_ids:
            self._preempt_seq(seq_id)

        seqs = []

        for seq_sched_metadata in scheduler_output.seq_schedule_metadata_list:
            self._on_seq_scheduled(seq_sched_metadata)
            seq = self.seq_map[seq_sched_metadata.seq_id]
            seqs.append(seq)

        return ignored_seqs, seqs

    @abstractmethod
    def _on_append_token(self, seq: Sequence, num_new_tokens: int) -> None:
        pass

    def _process_seq_output(
        self,
        seq: Sequence,
        sample: SamplerOutput,
    ) -> None:
        # at this point, the seq should be in paused state
        assert not seq.is_finished()

        if not seq.prompt_processing_finished:
            return

        for output_token in sample.output_tokens:
            seq.append_token_id(output_token)

        num_new_tokens = len(sample.output_tokens)

        self._on_append_token(seq, num_new_tokens)
        # this function will update the seq status

        # to finished if the stop condition is met
        seq.check_stop(num_new_tokens)
        if seq.is_finished():
            self._free_seq(seq.seq_id)

    @synchronized
    def on_step_completed(
        self,
        seq_schedule_metadata_list: List[SequenceScheduleMetadata],
        sampler_outputs: SamplerOutputs,
    ) -> None:
        for seq_schedule_metadata, sampler_output in zip(
            seq_schedule_metadata_list, sampler_outputs
        ):
            if not sampler_output:
                continue

            assert (
                seq_schedule_metadata.seq_id == sampler_output.seq_id
            ), f"{seq_schedule_metadata_list}, {sampler_outputs}"
            seq = self.seq_map[seq_schedule_metadata.seq_id]
            if seq.is_waiting_preempted():
                # seq is preempted
                # this can happen with pipeline parallel -- if the system
                # runs out of memory, it will preempt the last arrived request
                # this request might still be executing when the next stage scheduling
                # triggers the preemption
                continue

            if not seq.prompt_processing_finished:
                if not self.enable_sequence_pipeline_parallel:
                    # In case of sequence pipeline parallel, the stage token cursor is
                    # already updated in the on_stage_completed method
                    seq.update_prompt_tokens_stage_processed(
                        seq_schedule_metadata.num_q_tokens
                    )
                seq.update_prompt_tokens_processed(seq_schedule_metadata.num_q_tokens)

            if self.enable_sequence_pipeline_parallel:
                if not seq.prompt_stage_processing_finished:
                    # for prompts that are running in sequence parallel manner
                    # they would get unpaused at the end of the stage
                    pass
                elif (
                    seq.prompt_stage_processing_finished
                    and not seq.prompt_processing_finished
                ):
                    # this is the transition phase where the first stage has finished processing the prompt
                    # but there are intermediate micro-batches which are remaining before the prompt processing actually completes
                    pass
                elif seq.prompt_processing_finished:
                    self._pause_seq(seq_schedule_metadata.seq_id)
            else:
                self._pause_seq(seq_schedule_metadata.seq_id)

            self._process_seq_output(
                seq,
                sampler_output,
            )

    @synchronized
    def on_stage_completed(
        self,
        scheduler_output: SchedulerOutput,
    ) -> None:
        """
        This gets called only when pipeline parallel is enabled.
        The engine calls this when the first pipeline stage completed (engine-side) + each worker will
        call this method separately.
        """
        if not self.enable_sequence_pipeline_parallel:
            return

        for seq_schedule_metadata in scheduler_output.seq_schedule_metadata_list:
            seq = self.seq_map[seq_schedule_metadata.seq_id]
            assert not seq.is_finished()

            if seq.is_waiting_preempted():
                # seq is preempted
                # this can happen with pipeline parallel -- if the system
                # runs out of memory, it will preempt the last arrived request
                # this request might still be executing when the next stage scheduling
                # triggers the preemption
                continue

            if seq.prompt_stage_processing_finished:
                continue

            seq.update_prompt_tokens_stage_processed(seq_schedule_metadata.num_q_tokens)
            if not seq.prompt_stage_processing_finished:
                self._pause_seq(seq_schedule_metadata.seq_id)

    def generate_request_outputs(
        self,
        ignored_seqs: List[Sequence],
        seqs: List[Sequence],
    ) -> List[RequestOutput]:
        all_seqs = ignored_seqs + seqs
        return [RequestOutput.from_seq(seq) for seq in all_seqs]
