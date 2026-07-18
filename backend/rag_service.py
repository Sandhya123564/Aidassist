from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from pathlib import Patht
import os

CHROMA_DB = Path(_file_).parent / "chroma_db"

embeddings = None
db = None

def load_db():
    global embeddings, db

    if db is not None:
        return

    if not CHROMA_DB.exists():
        raise Exception(f"Chroma DB not found: {CHROMA_DB}")

    print("Loading embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Opening Chroma DB...")

    db = Chroma(
        persist_directory=str(CHROMA_DB),
        embedding_function=embeddings
    )

    print("Chroma DB opened.")