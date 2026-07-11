import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

KNOWLEDGE_BASE = "knowledge_base"
CHROMA_DB = "chroma_db"

documents = []

# Load all PDFs
for root, dirs, files in os.walk(KNOWLEDGE_BASE):
    for file in files:
        if file.endswith(".pdf"):
            path = os.path.join(root, file)
            print(f"Loading: {path}")
            loader = PyPDFLoader(path)
            documents.extend(loader.load())

print(f"Loaded {len(documents)} pages")
print(documents[0])
print("Content length:", len(documents[0].page_content))
print(documents[0].page_content[:300])

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

print("Chunks:", len(chunks))

if len(chunks) > 0:
    print(chunks[0].page_content[:300])

print(f"Created {len(chunks)} chunks")

# Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Save to ChromaDB
db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_DB
)

print("✅ Vector database created successfully!")