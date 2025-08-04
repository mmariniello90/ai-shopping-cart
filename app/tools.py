from openai import OpenAI
from dotenv import load_dotenv
from vector_db import create_chroma_persistent_client, create_collection


def get_similar_items(query_text: str, n_results: int = 2):
    load_dotenv()
    client = OpenAI()

    embedded_query = (
        client.embeddings.create(input=query_text, model="text-embedding-3-small")
        .data[0]
        .embedding
    )

    chroma_client = create_chroma_persistent_client(path="app/chroma_db")
    chroma_collection = create_collection(
        client=chroma_client, collection_name="app_collection"
    )

    retrieved_items = chroma_collection.query(
        query_embeddings=[embedded_query], n_results=n_results
    )

    return retrieved_items["metadatas"][0]


def manage_shopping_cart(shopping_cart: list, action: str, item: str) -> list:
    if action == "add":
        shopping_cart.append(item)
    elif action == "remove":
        shopping_cart.remove(item)
    else:
        print(f"Action {action} not allowed")

    return shopping_cart


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
                    "description": "The input query text to search for.",
                },
                "n_results": {
                    "type": "integer",
                    "description": "The number of top similar results to retrieve.",
                    "default": 2,
                },
            },
            "required": ["query_text"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "manage_shopping_cart",
        "description": "Add or remove items from the shopping cart.",
        "parameters": {
            "type": "object",
            "properties": {
                "shopping_cart": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "The list representing the shopping cart",
                },
                "action": {
                    "type": "string",
                    "description": "The action to apply in the cart. It can be add or remove.",
                },
                "item": {
                    "type": "string",
                    "description": "The item to add or remove from the cart.",
                },
            },
            "required": ["shopping_cart", "action", "item"],
            "additionalProperties": False,
        },
    },
]
