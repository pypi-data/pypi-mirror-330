from typing import List, Optional, Tuple

from vajra._native.datatypes import (
    LogicalTokenBlock,
    SamplerOutput,
    SamplingParams,
    SamplingType,
    SequenceMetadata,
    SequenceStatus,
)

from .comm_info import CommInfo
from .request_output import RequestOutput
from .scheduler_output import SchedulerOutput
from .sequence import Sequence
from .sequence_schedule_metadata import SequenceScheduleMetadata
from .sequence_state import SequenceState
from .tokenizer_protocol import TokenizerInput, TokenizerOutput
from .zmq_protocol import StepInputs, StepMicrobatchOutputs, StepOutputs

GPULocation = Tuple[Optional[str], int]  # (node_ip, gpu_id)
ResourceMapping = List[GPULocation]

SamplerOutputs = List[SamplerOutput]


__all__ = [
    "LogicalTokenBlock",
    "CommInfo",
    "RequestOutput",
    "SamplerOutput",
    "SamplerOutputs",
    "SamplingParams",
    "SchedulerOutput",
    "SequenceScheduleMetadata",
    "SequenceState",
    "SequenceStatus",
    "Sequence",
    "StepInputs",
    "StepMicrobatchOutputs",
    "StepOutputs",
    "SamplingType",
    "TokenizerInput",
    "TokenizerOutput",
    "GPULocation",
    "ResourceMapping",
    "SequenceMetadata",
]
