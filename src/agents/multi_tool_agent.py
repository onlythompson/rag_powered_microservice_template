from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.memory import ConversationBufferMemory
from src.llms import get_llm_model
from src.chains import ChainFactory
from src.core.config import settings
from src.core.observability import logger, trace_and_measure
from .base_agent import BaseAgent
import re

class MultiToolAgent(BaseAgent):
    def __init__(self):
        self.llm = get_llm_model(settings.LLM_MODEL_NAME)
        self.rag_chain = ChainFactory.get_chain("rag")
        self.summarization_chain = ChainFactory.get_chain("summarization")
        self.tools = [
            Tool(
                name="Query Knowledge Base",
                func=self.query_knowledge_base,
                description="Useful for when you need to answer questions about specific topics. Input should be a question."
            ),
            Tool(
                name="Summarize Text",
                func=self.summarize_text,
                description="Useful for when you need to summarize a long piece of text. Input should be the text to summarize."
            )
        ]
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent = LLMSingleActionAgent(
            llm_chain=self.llm,
            output_parser=self.output_parser,
            stop=["\nObservation:"],
            allowed_tools=[tool.name for tool in self.tools],
        )
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent, tools=self.tools, verbose=True, memory=self.memory
        )

    @trace_and_measure("query_knowledge_base")
    async def query_knowledge_base(self, query: str) -> str:
        result = await self.rag_chain.acall({"query": query})
        logger.info(f"Knowledge base queried: {query[:50]}...")
        return result['result']

    @trace_and_measure("summarize_text")
    async def summarize_text(self, text: str) -> str:
        result = await self.summarization_chain.acall({"text": text})
        logger.info(f"Text summarized: {text[:50]}...")
        return result['summary']

    @trace_and_measure("output_parser")
    def output_parser(self, llm_output: str):
        logger.info("Parsing LLM output")
        if "Final Answer:" in llm_output:
            return {"output": llm_output.split("Final Answer:")[-1].strip()}
        
        action_match = re.search(r"Action: (.*?)[\n]*Action Input: (.*)", llm_output, re.DOTALL)
        if not action_match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        
        action = action_match.group(1).strip()
        action_input = action_match.group(2).strip(" ").strip('"')
        return {"action": action, "action_input": action_input}

    @trace_and_measure("run")
    async def run(self, query: str) -> str:
        logger.info(f"Running Multi-Tool Agent with query: {query[:50]}...")
        return await self.agent_executor.run(query)
