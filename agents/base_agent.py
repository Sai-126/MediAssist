from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

class BaseAgent:
    def __init__(self):
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vectorstore = FAISS.load_local(
            "vector_store/",
            embedding_model,
            allow_dangerous_deserialization=True
        )

    def retrieve(self, query: str, k: int = 4) -> list:
        results = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
