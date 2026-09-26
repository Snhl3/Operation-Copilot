from app.rag.loader import load_documents


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def split_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
):
    """
    Split text into overlapping chunks.

    Args:
        text: Input document text.
        chunk_size: Maximum approximate number of characters per chunk.
        chunk_overlap: Number of characters shared between chunks.

    Returns:
        list[str]: List of text chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - chunk_overlap

    return chunks


def create_chunks(documents):
    """
    Create chunks from loaded documents while preserving metadata.

    Args:
        documents: Documents returned by load_documents().

    Returns:
        list[dict]: Chunk text with metadata.
    """

    chunks = []

    for document in documents:

        document_chunks = split_text(
            document["content"]
        )

        for chunk_index, chunk_text in enumerate(
            document_chunks
        ):

            chunk = {
                "content": chunk_text,
                "metadata": {
                    **document["metadata"],
                    "chunk_index": chunk_index,
                    "total_chunks": len(document_chunks),
                },
            }

            chunks.append(chunk)

    return chunks

def validate_chunks(chunks):
    """
    Perform basic validation on generated chunks.
    """

    if not chunks:
        raise ValueError("No chunks were generated.")

    for i, chunk in enumerate(chunks):

        content = chunk["content"]
        metadata = chunk["metadata"]

        if not content.strip():
            raise ValueError(
                f"Chunk {i} is empty."
            )

        if "source" not in metadata:
            raise ValueError(
                f"Chunk {i} is missing source metadata."
            )

        if "chunk_index" not in metadata:
            raise ValueError(
                f"Chunk {i} is missing chunk_index."
            )

    print("Chunk validation: PASS")


if __name__ == "__main__":

    documents = load_documents()

    chunks = create_chunks(documents)
    validate_chunks(chunks)


    print(f"Documents loaded: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")

    for chunk in chunks[:5]:

        print("\n-----------------------------")
        print(
            f"Source: {chunk['metadata']['source']}"
        )
        print(
            f"Chunk index: "
            f"{chunk['metadata']['chunk_index']}"
        )
        print(
            f"Total chunks in document: "
            f"{chunk['metadata']['total_chunks']}"
        )
        print(
            f"Characters: {len(chunk['content'])}"
        )
        print("\nContent:")
        print(chunk["content"][:500])