from rag_service import search_documents
import requests


def ask_local_rag(question):
    # 1. Retrieve relevant documents
    docs = search_documents(question)

    # 2. Combine retrieved document content
    context = "\n\n".join(doc.page_content for doc in docs)

    # 3. Create prompt for local Ollama model
    prompt = f"""
You are a helpful hearing-aid support assistant.

Answer the user's question using ONLY the information provided
in the context below.

If the answer is not available in the context, say:
"I could not find this information in the available hearing-aid manuals."

Context:
{context}

User question:
{question}

Answer:
"""

    # 4. Send prompt to Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"]


if __name__ == "__main__":
    question = "How do I clean my hearing aid?"

    answer = ask_local_rag(question)

    print("\n===== LOCAL RAG ANSWER =====\n")
    print(answer)