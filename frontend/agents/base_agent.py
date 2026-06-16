from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

class BaseAgent:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vectorstore = Chroma(
            persist_directory="vector_store/",
            embedding_function=self.embedding_model
        )

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