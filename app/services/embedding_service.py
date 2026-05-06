from langchain_huggingface import HuggingFaceEndpointEmbeddings
from app.config import HF_TOKEN



model = HuggingFaceEndpointEmbeddings(
    huggingfacehub_api_token = HF_TOKEN,
    model="sentence-transformers/all-MiniLM-L6-v2"
)

def generate_embeddings(docs:list):
    contents = [doc["content"] for doc in docs]

    embeddings = model.embed_documents(contents)     

    output = []

    for i,embed in enumerate(embeddings):
        output.append({
            "embedding":embed,
            "content": docs[i]["content"],
            "metadata":docs[i]["metadata"]
        })


    return output 

