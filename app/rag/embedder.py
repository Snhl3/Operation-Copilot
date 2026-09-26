from sentence_transformers import SentenceTransformer

from app.rag.loader import load_documents
from app.rag.chunker import create_chunks


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_embedding_model():
    """
    Load the local sentence-transformer embedding model.
    """

    return SentenceTransformer(MODEL_NAME)


def generate_embeddings(chunks, model):
    """
    Generate embeddings for document chunks.

    Args:
        chunks: List of chunk dictionaries.
        model: Loaded SentenceTransformer model.

    Returns:
        list: Embedding vectors.
    """

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
    )

    return embeddings

# check whether embeddings are correct or not

def validate_embeddings(chunks, embeddings):
    """
    Validate generated embeddings.
    """

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks does not match "
            "number of embeddings."
        )

    if len(embeddings) == 0:
        raise ValueError(
            "No embeddings were generated."
        )

    if embeddings.shape[1] != 384:
        raise ValueError(
            f"Unexpected embedding dimension: "
            f"{embeddings.shape[1]}"
        )

    print("Embedding validation: PASS")

if __name__ == "__main__":

    documents = load_documents()

    chunks = create_chunks(documents)

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    model = load_embedding_model()

    embeddings = generate_embeddings(
        chunks,
        model,
    )

    validate_embeddings(
        chunks,
        embeddings,
    )

    print("\nEmbedding generation completed.")

    print(
        f"Number of embeddings: {len(embeddings)}"
    )

    print(
        f"Embedding dimensions: {embeddings.shape[1]}"
    )

    print(
        f"First embedding shape: {embeddings[0].shape}"
    )

    print(
        "\nFirst 10 values of first embedding:"
    )

    print(embeddings[0][:10])