from app.rag.loader import load_documents
from app.rag.chunker import create_chunks


KEYWORDS = [
    "abnormal",
    "investigation",
    "corrective",
    "shutdown",
    "stop",
    "report",
]


def main():
    documents = load_documents()
    chunks = create_chunks(documents)

    print("\n" + "=" * 80)
    print("EQUIPMENT SOP RELEVANT CHUNKS")
    print("=" * 80)

    for chunk in chunks:
        metadata = chunk["metadata"]

        if metadata["source"] != "equipment_operating_sop.md":
            continue

        content_lower = chunk["content"].lower()

        matched_keywords = [
            keyword
            for keyword in KEYWORDS
            if keyword in content_lower
        ]

        if matched_keywords:
            print("\n" + "-" * 80)
            print(
                f"Chunk index: "
                f"{metadata['chunk_index']}"
            )
            print(
                f"Matched keywords: "
                f"{', '.join(matched_keywords)}"
            )
            print("\nContent:")
            print(chunk["content"])


if __name__ == "__main__":
    main()