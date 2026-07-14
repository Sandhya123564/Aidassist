from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

print("Loading embeddings...")

CHROMA_DB = "chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embeddings loaded.")

print("Opening Chroma DB...")

db = Chroma(
    persist_directory=CHROMA_DB,
    embedding_function=embeddings
)

print("Chroma DB opened.")

def search_documents(query):
    print("Searching for:", query)

    docs = db.similarity_search(query, k=3)

    print("Documents found:", len(docs))

    if docs:
        print("First document:", docs[0].page_content[:200])

    return docs