import chromadb


def create_chrome_client():
    return chromadb.Client()


def create_chroma_persistent_client(path: str):
    return chromadb.PersistentClient(path=path)


def create_collection(client, collection_name: str):
    return client.get_or_create_collection(name=collection_name)

