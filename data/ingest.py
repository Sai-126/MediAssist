from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

loaders = [
    PyPDFLoader("data/raw/nhm_guidelines.pdf"),
    PyPDFLoader("data/raw/pmjay.pdf"),
    PyPDFLoader("data/raw/Communicable Diseases.pdf"),
    PyPDFLoader("data/raw/Guidebook for Medical Officer.pdf"),
    PyPDFLoader("data/raw/Guidelines_CommonIllness.pdf"),
    PyPDFLoader("data/raw/WHO medical list.pdf"),
    TextLoader("data/raw/medical_faqs.txt", encoding="utf-8"),
]

docs = []
for loader in loaders:
    try:
        docs.extend(loader.load())
        print(f"Loaded successfully")
    except Exception as e:
        print(f"Error: {e}")

print(f"Total documents loaded: {len(docs)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " "]
)
chunks = splitter.split_documents(docs)
print(f"Total chunks created: {len(chunks)}")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = FAISS.from_documents(chunks, embedding_model)
vectorstore.save_local("vector_store/")
print("Vector store built and saved!")
