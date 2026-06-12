from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = FAISS.load_local(
    "vector_store/",
    embedding_model,
    allow_dangerous_deserialization=True
)

test_queries = [
    "What is Aarogyasri scheme eligibility?",
    "Side effects of paracetamol",
    "Symptoms of diabetes",
    "PM-JAY scheme benefits",
    "What is metformin used for?",
]

for query in test_queries:
    print(f"\nQuery: {query}")
    print("-" * 50)
    results = vectorstore.similarity_search(query, k=3)
    for i, doc in enumerate(results):
        print(f"  [{i+1}] {doc.page_content[:200]}...")
