from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from src.services import QueryService
from src.core.config import settings

class AdvancedRAGChain:
    def __init__(self):
        self.query_service = QueryService()
        self.llm = ChatOpenAI(temperature=0, model_name=settings.MODEL_NAME)

    async def run(self, query: str) -> str:
        # First, get relevant documents
        retrieval_result = await self.query_service.process_query(query)
        context = "\n".join(retrieval_result['source_documents'])

        # Then, use an LLM to generate a more comprehensive answer
        prompt = PromptTemplate(
            input_variables=["context", "query"],
            template="""
            You are an AI assistant tasked with providing comprehensive and accurate answers.
            Use the following context to answer the question. If the context doesn't contain
            enough information, you can use your general knowledge, but clearly indicate when
            you're doing so.

            Context:
            {context}

            Human: {query}
            AI: Let's break this down step by step:
            """
        )

        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = await chain.arun(context=context, query=query)
        
        return response