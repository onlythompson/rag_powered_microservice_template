from abc import ABC, abstractmethod
from src.core.observability import logger, trace_and_measure

class BaseAgent(ABC):
    @abstractmethod
    async def run(self, *args, **kwargs):
        pass

    @trace_and_measure("agent_step")
    async def step(self, *args, **kwargs):
        logger.info(f"Agent step: {self.__class__.__name__}")
        return await self.run(*args, **kwargs)