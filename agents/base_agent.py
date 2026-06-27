from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

class BaseAgent:
    _embedding_model = None
    _vectorstore = None

    def __init__(self):
        if BaseAgent._embedding_model is None:
            BaseAgent._embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"}
            )
        if BaseAgent._vectorstore is None:
            BaseAgent._vectorstore = Chroma(
                persist_directory="vector_store/",
                embedding_function=BaseAgent._embedding_model
            )
        self.vectorstore = BaseAgent._vectorstore

    def retrieve(self, query: str, k: int = 4) -> list:
        results = self.vectorstore.similarity_search(query, k=k)
        docs = []
        for doc in results:
            source = doc.metadata.get("source", "unknown document")
            docs.append({
                "content": doc.page_content,
                "source": source
            })
        return docs

    def format_context(self, docs: list) -> str:
        context = ""
        for doc in docs:
            context += f"[Source: {doc['source']}]\n{doc['content']}\n\n"
        return context.strip()