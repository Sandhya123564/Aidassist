from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DB = str(Path(__file__).parent / "chroma_db")

embeddings = None
db = None


def load_db():
    global embeddings, db

    if db is not None:
        return

    if not Path(CHROMA_DB).exists():
        raise Exception(f"Chroma DB not found: {CHROMA_DB}")

    print("Loading MPNet embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    print("Opening Chroma DB...")

    db = Chroma(
        persist_directory=CHROMA_DB,
        embedding_function=embeddings
    )

    print("Chroma DB opened.")


def search_documents(query):
    load_db()

    print("RAG SEARCH QUERY:", query)

    docs = db.similarity_search(query, k=3)

    print("RAG DOCUMENTS FOUND:", len(docs))

    for i, doc in enumerate(docs):
        print(f"RAG DOC {i}:")
        print(doc.page_content[:500])

    return docs