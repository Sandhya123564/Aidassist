from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DB = "chroma_db"

embeddings = None
db = None

def load_db():
    global embeddings, db

    if db is None:
        print("Loading embeddings...")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Opening Chroma DB...")

        db = Chroma(
            persist_directory=CHROMA_DB,
            embedding_function=embeddings
        )

        print("Chroma DB opened.")

def search_documents(query):
    load_db()

    docs = db.similarity_search(query, k=3)
    return docs