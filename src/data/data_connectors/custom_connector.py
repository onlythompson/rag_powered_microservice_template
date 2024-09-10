import requests
from typing import List, Dict, Any
from langchain.docstore.document import Document
from sqlalchemy import create_engine, text

class DatabaseConnector:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)

    def fetch_data(self, query: str) -> List[Document]:
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            documents = []
            for row in result:
                content = " ".join(f"{k}: {v}" for k, v in row._mapping.items())
                doc = Document(page_content=content, metadata={"source": "database", "query": query})
                documents.append(doc)
        return documents

class APIConnector:
    def __init__(self, base_url: str, headers: Dict[str, str] = None):
        self.base_url = base_url
        self.headers = headers or {}

    def fetch_data(self, endpoint: str, params: Dict[str, Any] = None) -> List[Document]:
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        documents = []
        for item in data:
            content = str(item)  # Convert the entire item to a string
            doc = Document(page_content=content, metadata={"source": "api", "endpoint": endpoint})
            documents.append(doc)
        return documents