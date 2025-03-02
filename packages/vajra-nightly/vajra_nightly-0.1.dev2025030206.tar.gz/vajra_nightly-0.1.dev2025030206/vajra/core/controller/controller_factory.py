from vajra.config import LLMReplicaControllerConfig
from vajra.core.controller.abstract_controller import AbstractController
from vajra.core.controller.base_llm_replica_controller import BaseLLMReplicaController
from vajra.core.controller.pipeline_parallel_llm_replica_controller import (
    PipelineParallelLLMReplicaController,
)


class ControllerFactory:
    """Factory class for creating Vajra controllers based on configuration."""

    @classmethod
    def create_controller(
        cls, config: LLMReplicaControllerConfig
    ) -> AbstractController:
        """Creates an appropriate Vajra controller based on the system configuration.

        Args:
            config: The system configuration specifying model, parallel strategy etc.

        Returns:
            An instance of AbstractController based on the parallel config.
        """
        if config.parallel_config.pipeline_parallel_size > 1:
            return PipelineParallelLLMReplicaController(config)
        else:
            return BaseLLMReplicaController(config)
