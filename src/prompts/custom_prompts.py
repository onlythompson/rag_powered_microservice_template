from langchain.prompts import PromptTemplate

def get_qa_prompt() -> PromptTemplate:
    template = """You are an AI assistant tasked with answering questions based on the given context. 
    Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context:
    {context}

    Question: {question}
    Answer: """
    return PromptTemplate(template=template, input_variables=["context", "question"])

def get_summarization_prompt() -> PromptTemplate:
    template = """Summarize the following text in a concise manner, capturing the main points and key details:

    Text: {text}

    Summary: """
    return PromptTemplate(template=template, input_variables=["text"])

def get_entity_extraction_prompt() -> PromptTemplate:
    template = """Extract and list all named entities (such as people, organizations, locations, etc.) from the following text:

    Text: {text}

    Entities:
    """
    return PromptTemplate(template=template, input_variables=["text"])

def get_fact_checking_prompt() -> PromptTemplate:
    template = """Given the following claim and context, determine if the claim is supported by the context, contradicted by the context, or if there's not enough information to make a determination.

    Claim: {claim}

    Context: {context}

    Analysis:
    1. Is the claim supported by the context? (Yes/No/Insufficient Information)
    2. Explanation: 

    """
    return PromptTemplate(template=template, input_variables=["claim", "context"])