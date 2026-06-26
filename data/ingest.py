from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
import glob

RAW_DIR = "data/raw/"
VECTOR_DIR = "vector_store/"

print("Loading documents...")
docs = []

pdf_files = glob.glob(os.path.join(RAW_DIR, "**/*.pdf"), recursive=True)
txt_files = glob.glob(os.path.join(RAW_DIR, "**/*.txt"), recursive=True)

for pdf_path in pdf_files:
    try:
        loader = PyPDFLoader(pdf_path)
        loaded = loader.load()
        docs.extend(loaded)
        print(f"Loaded: {os.path.basename(pdf_path)} ({len(loaded)} pages)")
    except Exception as e:
        print(f"SKIPPED (corrupted/unreadable): {os.path.basename(pdf_path)} - {str(e)[:100]}")

for txt_path in txt_files:
    try:
        loader = TextLoader(txt_path, encoding="utf-8")
        loaded = loader.load()
        docs.extend(loaded)
        print(f"Loaded: {os.path.basename(txt_path)}")
    except Exception as e:
        print(f"SKIPPED: {os.path.basename(txt_path)} - {str(e)[:100]}")

print(f"\nTotal documents loaded: {len(docs)}")

for doc in docs:
    doc.metadata["source"] = os.path.basename(
        doc.metadata.get("source", "unknown")
    )

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

print("Building vector store...")
vectorstore = Chroma.from_documents(
    chunks,
    embedding_model,
    persist_directory=VECTOR_DIR
)
print(f"Vector store saved to {VECTOR_DIR}")
print("Done!")