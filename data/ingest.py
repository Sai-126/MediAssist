from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

RAW_DIR = "data/raw/"
VECTOR_DIR = "vector_store/"

print("Loading documents...")
pdf_loader = DirectoryLoader(RAW_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
txt_loader = DirectoryLoader(RAW_DIR, glob="**/*.txt", loader_cls=TextLoader,
                               loader_kwargs={"encoding": "utf-8"})

docs = pdf_loader.load() + txt_loader.load()
print(f"Total documents loaded: {len(docs)}")

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