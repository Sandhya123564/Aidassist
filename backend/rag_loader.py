from langchain_community.document_loaders import PyPDFLoader
import os

# Folder containing all PDFs
KNOWLEDGE_BASE = "knowledge_base"

documents = []

# Read all PDFs from knowledge_base
for root, dirs, files in os.walk(KNOWLEDGE_BASE):
    for file in files:
        if file.endswith(".pdf"):
            pdf_path = os.path.join(root, file)
            print(f"Loading: {pdf_path}")

            loader = PyPDFLoader(pdf_path)
            docs = loader.load()

            documents.extend(docs)

print(f"\nTotal pages loaded: {len(documents)}")