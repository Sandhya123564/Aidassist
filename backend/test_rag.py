from rag_service import search_documents

query = "How do I clean my hearing aid?"

results = search_documents(query)

print(f"Found {len(results)} results")

for i, doc in enumerate(results, 1):
    print(f"\n----- Result {i} -----")
    print(doc.page_content[:500])