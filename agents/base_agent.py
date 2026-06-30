from langchain_chroma import Chroma
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
load_dotenv()

class BaseAgent:
    _vectorstore = None
    _embedding_fn = None

    def __init__(self):
        if BaseAgent._embedding_fn is None:
            BaseAgent._embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        if BaseAgent._vectorstore is None:
            import chromadb
            client = chromadb.PersistentClient(path="vector_store/")
            collections = client.list_collections()
            collection_name = collections[0].name if collections else "langchain"
            BaseAgent._vectorstore = client.get_collection(
                name=collection_name,
                embedding_function=BaseAgent._embedding_fn
            )
        self.collection = BaseAgent._vectorstore

    def retrieve(self, query: str, k: int = 4) -> list:
        results = self.collection.query(query_texts=[query], n_results=k)
        docs = []
        if results and results.get("documents"):
            for i, content in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i] if results.get("metadatas") else {}
                source = metadata.get("source", "unknown document")
                docs.append({"content": content, "source": source})
        return docs

    def format_context(self, docs: list) -> str:
        context = ""
        for doc in docs:
            context += f"[Source: {doc['source']}]\n{doc['content']}\n\n"
        return context.strip()