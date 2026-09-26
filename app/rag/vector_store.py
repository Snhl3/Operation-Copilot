from pathlib import Path

import chromadb

from app.rag.loader import load_documents
from app.rag.chunker import create_chunks
from app.rag.embedder import (
    load_embedding_model,
    generate_embeddings,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store"

COLLECTION_NAME = "industrial_sop_documents"


def get_chroma_client():
    """
    Create a persistent ChromaDB client.
    """

    VECTOR_STORE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    client = chromadb.PersistentClient(
        path=str(VECTOR_STORE_DIR)
    )

    return client


def get_collection(client):
    """
    Get or create the industrial SOP collection.
    """

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def build_vector_store():

    documents = load_documents()

    chunks = create_chunks(documents)

    model = load_embedding_model()

    embeddings = generate_embeddings(
        chunks,
        model,
    )

    client = get_chroma_client()

    collection = get_collection(client)

    ids = []
    texts = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        chunk_id = (
            f"{chunk['metadata']['source']}"
            f"__chunk_{chunk['metadata']['chunk_index']}"
        )

        ids.append(chunk_id)

        texts.append(
            chunk["content"]
        )

        metadatas.append(
            chunk["metadata"]
        )

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
    )

    print("Vector store created successfully.")
    print(
        f"Documents: {len(documents)}"
    )
    print(
        f"Chunks stored: {len(chunks)}"
    )
    print(
        f"Collection: {COLLECTION_NAME}"
    )


if __name__ == "__main__":
    build_vector_store()