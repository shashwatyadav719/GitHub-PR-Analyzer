import chromadb
from chromadb.config import Settings
from app.services.embedding_service import model




client = chromadb.Client(
    Settings(
        persist_directory="chroma_db",
        is_persistent=True
    )
)


collection = client.get_or_create_collection(
    name="pr_chunks"
)


def store_embeddings(embed_docs:list):

    if not embed_docs:
        return {"message": "No embeddings to store"}
    
    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for i,doc in enumerate(embed_docs):
        meta = doc.get("metadata")
        content = doc.get("content")
        embedding = doc.get("embedding")

        if not meta or not content or not embedding:
            continue

        unique_id = f"{meta['github_user_id']}_{meta['repo_name']}_{meta['pr_number']}_{meta['file_name']}_{i}"

        ids.append(unique_id)
        documents.append(content)
        metadatas.append(meta)
        embeddings.append(embedding)

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    

    return {"message": "Embeddings stored successfully"}

def query_embeddings(query:str,github_id:int,repo_name:str,pr_number:int,top_k=8):
    query_embedding = model.embed_query(query)

    if not query.strip():
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where = {
            "$and": [
                {"github_user_id": github_id},
                {"repo_name": repo_name},
                {"pr_number": pr_number}
            ]
        }
    )

    docs = results.get("documents")

    if not docs or len(docs) == 0 or len(docs[0]) == 0:
        return []

    return docs[0]

def check_pr_exists(github_user_id: int, repo_name: str, pr_number: int):
    results = collection.get(
        where={
            "$and": [
                {"github_user_id": github_user_id},
                {"repo_name": repo_name},
                {"pr_number": pr_number}
            ]
        },
        limit=1
    )

    ids = results.get("ids")

    if ids is None:
        return False

    if len(ids) == 0:
        return False

    return True