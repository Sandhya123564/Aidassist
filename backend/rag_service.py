#from langchain_community.vectorstores import Chroma
#from langchain_community.embeddings import HuggingFaceEmbeddings

#CHROMA_DB = "chroma_db"

#embeddings = HuggingFaceEmbeddings(
   # model_name="sentence-transformers/all-MiniLM-L6-v2"
#)

#db = Chroma(
 #   persist_directory=CHROMA_DB,
  #  embedding_function=embeddings
#)

def search_documents(query):
    docs = db.similarity_search(query, k=3)
    return docs