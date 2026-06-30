from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions
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
        print(f"SKIPPED: {os.path.basename(pdf_path)} - {str(e)[:100]}")

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
    doc.metadata["source"] = os.path.basename(doc.metadata.get("source", "unknown"))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " "]
)
chunks = splitter.split_documents(docs)
print(f"Total chunks created: {len(chunks)}")

print("Building vector store...")
client = chromadb.PersistentClient(path=VECTOR_DIR)
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="mediassist",
    embedding_function=embedding_fn
)

batch_size = 200
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i+batch_size]
    collection.add(
        documents=[c.page_content for c in batch],
        metadatas=[c.metadata for c in batch],
        ids=[f"chunk_{i+j}" for j in range(len(batch))]
    )
    print(f"  Added {min(i+batch_size, len(chunks))}/{len(chunks)} chunks")

print(f"Vector store saved to {VECTOR_DIR}")
print("Done!")