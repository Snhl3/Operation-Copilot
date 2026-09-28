from app.rag.vector_store import (
    get_chroma_client,
    get_collection,
)
from app.rag.embedder import (
    load_embedding_model,
)


def search_documents(
    query: str,
    top_k: int = 3,
    model=None,
):
    """
    Search the ChromaDB collection using
    semantic similarity.

    The embedding model can be passed in so that
    callers performing multiple searches can reuse
    the same model instance.
    """

    if model is None:
        model = load_embedding_model()

    query_embedding = model.encode(
        [query]
    )[0]

    client = get_chroma_client()
    collection = get_collection(client)

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k,
    )

    return results


if __name__ == "__main__":
    query = (
        "What should I check before "
        "starting production?"
    )

    model = load_embedding_model()

    results = search_documents(
        query=query,
        top_k=3,
        model=model,
    )

    print("\nQuery:")
    print(query)

    print("\nRetrieved documents:")

    for i, document in enumerate(
        results["documents"][0]
    ):
        print("\n-----------------------------")
        print(f"Rank: {i + 1}")
        print(
            f"Distance: "
            f"{results['distances'][0][i]}"
        )
        print(
            f"Source: "
            f"{results['metadatas'][0][i]['source']}"
        )
        print(
            f"Chunk: "
            f"{results['metadatas'][0][i]['chunk_index']}"
        )
        print("\nContent:")
        print(document)