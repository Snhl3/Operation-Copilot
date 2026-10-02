from app.rag.embedder import load_embedding_model
from app.rag.retriever import search_documents


QUESTIONS = [
    "What should be done when visible equipment damage is identified?",
    "What should be done when production conditions indicate abnormal equipment behavior?",
    "What should be verified before operating the equipment?",
]


def main():
    model = load_embedding_model()

    for question in QUESTIONS:
        results = search_documents(
            query=question,
            top_k=3,
            model=model,
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        print("\n" + "=" * 80)
        print("RETRIEVAL DEBUG")
        print("=" * 80)

        print(f"\nQuestion:\n{question}")

        for rank, (document, metadata, distance) in enumerate(
            zip(documents, metadatas, distances),
            start=1,
        ):
            print("\n" + "-" * 80)
            print(f"Rank: {rank}")
            print(f"Source: {metadata['source']}")
            print(f"Chunk index: {metadata['chunk_index']}")
            print(f"Distance: {distance:.4f}")
            print("\nContent:")
            print(document)


if __name__ == "__main__":
    main()
