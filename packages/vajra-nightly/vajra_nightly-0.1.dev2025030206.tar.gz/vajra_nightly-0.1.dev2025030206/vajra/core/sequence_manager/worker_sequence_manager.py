from collections import defaultdict
from typing import Dict, List, Tuple

from vajra.config import LLMReplicaControllerConfig
from vajra.core.block_space_manager import BlockSpaceManager
from vajra.core.sequence_manager.base_sequence_manager import BaseSequenceManager
from vajra.datatypes import SamplerOutputs  # type: ignore
from vajra.datatypes import SequenceMetadata  # type: ignore
from vajra.datatypes import (
    SchedulerOutput,
    Sequence,
    SequenceScheduleMetadata,
)
from vajra.logger import init_logger
from vajra.model_executor.layers.attention.sequence_arrangement import (
    SequenceArrangement,
)
from vajra.model_executor.parallel_utils.parallel_state import (
    get_kv_parallel_rank,
    get_kv_parallel_world_size,
    get_rank,
)
from vajra.utils.threading_utils import synchronized

logger = init_logger(__name__)


class WorkerSequenceManager(BaseSequenceManager):

    def __init__(
        self,
        config: LLMReplicaControllerConfig,
    ):
        super().__init__(config)
        # we will have a clone of block manager here, it is supposed
        # to work in sync block manager in scheduler the idea is to avoid
        # sending block table every time to the worker
        self.rank = get_rank()
        self.kvp_group_id = get_kv_parallel_rank()

        if get_kv_parallel_world_size() == 1:
            self.max_num_tokens_per_kvp_group = config.model_config.max_model_len
        else:
            self.max_num_tokens_per_kvp_group = (
                config.parallel_config.max_num_tokens_per_kvp_group
            )

        self.seq_num_processed_tokens_map: Dict[str, int] = defaultdict(int)

        assert config.cache_config.num_gpu_blocks is not None
        self.block_manager = BlockSpaceManager(
            config.cache_config.block_size,
            config.cache_config.num_gpu_blocks,
            config.model_config.max_model_len,
        )

    def _free_seq(self, seq_id: str) -> None:
        # ignored sequences might not have been allocated
        assert seq_id in self.seq_map
        seq = self.seq_map[seq_id]
        if self.block_manager.is_allocated(seq):
            self.block_manager.free(seq)
        super()._free_seq(seq_id)

    def _preempt_seq(self, seq_id: str) -> None:
        super()._preempt_seq(seq_id)
        seq = self.seq_map[seq_id]
        if self.block_manager.is_allocated(seq):
            self.block_manager.free(seq)

    def _on_seq_scheduled(
        self,
        seq_sched_metadata: SequenceScheduleMetadata,
    ) -> None:
        assert seq_sched_metadata.seq_id in self.seq_map
        self._resume_seq(seq_sched_metadata.seq_id)

        seq = self.seq_map[seq_sched_metadata.seq_id]
        num_total_blocks = seq_sched_metadata.kvp_group_block_counter[self.kvp_group_id]
        logger.debug(
            f"Allocating {num_total_blocks} blocks for seq {seq.seq_id} in group {self.kvp_group_id}"
        )
        self.block_manager.allocate_delta(seq, num_total_blocks)

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

            self._update_seq_num_processed_tokens_map(seq, seq_schedule_metadata)

            seq.update_prompt_tokens_stage_processed(seq_schedule_metadata.num_q_tokens)

            if (
                self.kvp_group_id in seq_schedule_metadata.kvp_group_ids
                and not seq.prompt_stage_processing_finished
            ):
                self._pause_seq(seq_schedule_metadata.seq_id)

    @synchronized
    def on_step_completed(
        self,
        seq_schedule_metadata_list: List[SequenceScheduleMetadata],
        sampler_outputs: SamplerOutputs,
    ) -> None:
        filtered_seq_metadata_list = []
        sorted_sampler_outputs = []
        sampler_outputs_map = {s.seq_id: s for s in sampler_outputs if s}

        for seq_sched_metadata in seq_schedule_metadata_list:
            seq = self.seq_map[seq_sched_metadata.seq_id]

            assert not seq.is_finished()

            if (
                not self.kvp_group_id in seq_sched_metadata.kvp_group_ids
                and not seq.prompt_processing_finished
            ):
                if not self.enable_sequence_pipeline_parallel:
                    # In case of sequence pipeline parallel, the stage token cursor is
                    # already updated in the on_stage_completed method
                    seq.update_prompt_tokens_stage_processed(
                        seq_sched_metadata.num_q_tokens
                    )
                seq.update_prompt_tokens_processed(seq_sched_metadata.num_q_tokens)
                continue

            if (
                not self.enable_sequence_pipeline_parallel
                or seq.prompt_processing_finished
            ):
                # in case of sequence pipeline parallel, the stage token cursor is
                # already updated in the on_stage_completed method
                self._update_seq_num_processed_tokens_map(seq, seq_sched_metadata)

            if not self.kvp_group_id in seq_sched_metadata.kvp_group_ids:
                continue

            filtered_seq_metadata_list.append(seq_sched_metadata)
            sorted_sampler_outputs.append(sampler_outputs_map[seq.seq_id])

        super().on_step_completed(filtered_seq_metadata_list, sorted_sampler_outputs)

    def _on_append_token(self, seq: Sequence, num_new_tokens: int) -> None:
        # the engine performs detokenization at this point
        # but we don't need to do anything here on worker side
        pass

    def _get_block_table(self, seq: Sequence) -> List[int]:
        return self.block_manager.get_block_table(seq)

    def _update_seq_num_processed_tokens_map(
        self,
        seq: Sequence,
        seq_sched_metadata: SequenceScheduleMetadata,
    ) -> None:
        if self.kvp_group_id != seq_sched_metadata.kvp_group_ids[-1]:
            return

        if not seq.prompt_stage_processing_finished:
            self.seq_num_processed_tokens_map[
                seq.seq_id
            ] += seq_sched_metadata.num_q_tokens
            assert (
                self.seq_num_processed_tokens_map[seq.seq_id]
                <= self.max_num_tokens_per_kvp_group
            ), (
                f"seq_id: {seq.seq_id}, "
                f"num_processed_tokens: {self.seq_num_processed_tokens_map[seq.seq_id]}, "
                f"max_num_tokens_per_kvp_group: {self.max_num_tokens_per_kvp_group}"
            )
        else:
            self.seq_num_processed_tokens_map[seq.seq_id] += 1

    def on_schedule(
        self,
        scheduler_output: SchedulerOutput,
    ) -> Tuple[List[Sequence], List[Sequence]]:
        raise NotImplementedError

    @synchronized
    def on_schedule_worker(
        self,
        scheduler_output: SchedulerOutput,
    ) -> Tuple[List[Sequence], List[Sequence], List[SequenceMetadata]]:
        ignored_seqs: List[Sequence] = []
        for seq_id in scheduler_output.ignored_seq_ids:
            assert seq_id in self.seq_map
            seq = self.seq_map[seq_id]
            ignored_seqs.append(seq)
            self._free_seq(seq_id)

        for seq_id in scheduler_output.preempted_seq_ids:
            self._preempt_seq(seq_id)

        seq_metadata_list: List[SequenceMetadata] = []

        for seq_sched_metadata in scheduler_output.seq_schedule_metadata_list:
            assert seq_sched_metadata.seq_id in self.seq_map, (
                f"seq_id {seq_sched_metadata.seq_id} not found in seq_map. "
                f"seq_map: {self.seq_map} for rank {self.rank}"
            )

            if not self.kvp_group_id in seq_sched_metadata.kvp_group_ids:
                continue

            seq = self.seq_map[seq_sched_metadata.seq_id]

            self._on_seq_scheduled(seq_sched_metadata)

            kv_cache_len = self.seq_num_processed_tokens_map[seq.seq_id]
            save_kv_cache = self.kvp_group_id == seq_sched_metadata.kvp_group_ids[-1]

            seq_metadata = SequenceMetadata(
                seq_sched_metadata.schedule_id,
                seq.seq_id,
                seq_sched_metadata.num_q_tokens,
                kv_cache_len,
                self._get_block_table(seq),
                seq_sched_metadata.kvp_group_ids,
                save_kv_cache,
            )
            seq_metadata_list.append(seq_metadata)

        seq_arrangement = SequenceArrangement()
        seq_arrangement.extend(seq_metadata_list)
        seq_metadata_list = seq_arrangement.get_arranged()

        seqs = [self.seq_map[seq_metadata.seq_id] for seq_metadata in seq_metadata_list]

        return ignored_seqs, seqs, seq_metadata_list
