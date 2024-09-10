from abc import ABC, abstractmethod
from langchain.chains.base import Chain
from src.core.observability import logger, trace_and_measure

class BaseChain(Chain, ABC):
    @abstractmethod
    async def _acall(self, inputs: dict) -> dict:
        pass

    @trace_and_measure("chain_run")
    async def acall(self, inputs: dict) -> dict:
        logger.info(f"Running chain: {self.__class__.__name__}")
        return await self._acall(inputs)