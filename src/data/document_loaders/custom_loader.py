import csv
from typing import List
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document

class CustomPDFLoader(PyPDFLoader):
    def __init__(self, file_path: str):
        super().__init__(file_path)

    def load(self) -> List[Document]:
        documents = super().load()
        # Add custom processing here, e.g., adding metadata
        for doc in documents:
            doc.metadata["source_type"] = "pdf"
        return documents

class CustomCSVLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Document]:
        documents = []
        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                content = " ".join(f"{k}: {v}" for k, v in row.items())
                doc = Document(page_content=content, metadata={"source": self.file_path, "source_type": "csv"})
                documents.append(doc)
        return documents# src/data/document_loaders/custom_loader.py

