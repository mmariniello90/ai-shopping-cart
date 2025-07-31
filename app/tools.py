from openai import OpenAI
from dotenv import load_dotenv
from vector_db import create_chroma_persistent_client, create_collection

def get_similar_items(query_text: str, n_results: int = 2):

    load_dotenv()
    client = OpenAI()

    embedded_query = client.embeddings.create(
        input=query_text,
        model="text-embedding-3-small"
    ).data[0].embedding

    chroma_client = create_chroma_persistent_client(path="app/chroma_db")
    chroma_collection = create_collection(client=chroma_client, collection_name="app_collection")



    retrieved_items = chroma_collection.query(
        query_embeddings=[embedded_query],
        n_results=n_results
    )

    return retrieved_items["metadatas"][0]

tools = [
    {
        "type": "function",
        "name": "get_similar_items",
        "description": "Search for semantically similar text items in ChromaDB using OpenAI embeddings.",
        "parameters": {
            "type": "object",
            "properties": {
                "query_text": {
                    "type": "string",
                    "description": "The input query text to search for."
                },
                "n_results": {
                    "type": "integer",
                    "description": "The number of top similar results to retrieve.",
                    "default": 2
                }
            },
            "required": [
                "query_text"
            ],
            "additionalProperties": False
        }
    }

]





