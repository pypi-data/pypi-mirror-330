from typing import List, Union

from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast

from vajra.config import LLMReplicaControllerConfig
from vajra.core.sequence_manager.base_sequence_manager import BaseSequenceManager
from vajra.datatypes import Sequence
from vajra.transformers_utils.tokenizer import detokenize_incrementally

INCREMENTAL_DETOKENIZATION_WINDOW = 5


class EngineSequenceManager(BaseSequenceManager):

    def __init__(
        self,
        tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
        config: LLMReplicaControllerConfig,
    ):
        super().__init__(config)
        self.tokenizer = tokenizer

    def _decode_seq(self, seq: Sequence, num_new_tokens: int) -> None:
        """Decodes the new token for a sequence."""
        (new_tokens, new_output_text, prefix_offset, read_offset) = (
            detokenize_incrementally(
                self.tokenizer,
                last_five_input_ids=seq.get_last_n_token_ids(
                    INCREMENTAL_DETOKENIZATION_WINDOW + num_new_tokens - 1
                ),
                prev_tokens=seq.tokens,
                prefix_offset=seq.prefix_offset,
                read_offset=seq.read_offset,
                skip_special_tokens=True,
            )
        )
        if seq.tokens is None:
            seq.tokens = new_tokens
        else:
            seq.tokens.extend(new_tokens)
        seq.prefix_offset = prefix_offset
        seq.read_offset = read_offset
        seq.output_text += new_output_text

    def _on_append_token(self, seq: Sequence, num_new_tokens: int) -> None:
        self._decode_seq(seq, num_new_tokens)

    def _get_block_table(self, seq: Sequence) -> List[int]:
        return []
