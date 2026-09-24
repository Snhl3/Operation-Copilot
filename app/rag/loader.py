from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = PROJECT_ROOT / "documents"


def load_documents():
    """
    Load all Markdown documents from the documents directory.

    Returns:
        list[dict]: Each document contains content and metadata.
    """

    if not DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            f"Documents directory not found: {DOCUMENTS_DIR}"
        )

    documents = []

    for file_path in sorted(DOCUMENTS_DIR.glob("*.md")):

        content = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not content:
            raise ValueError(
                f"Document is empty: {file_path.name}"
            )

        document = {
            "content": content,
            "metadata": {
                "source": file_path.name,
                "file_path": str(file_path),
                "file_type": file_path.suffix,
            },
        }

        documents.append(document)

    if not documents:
        raise ValueError(
            f"No Markdown documents found in {DOCUMENTS_DIR}"
        )

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    for document in documents:

        print("\n-----------------------------")
        print(f"Source: {document['metadata']['source']}")
        print(f"Type: {document['metadata']['file_type']}")
        print(f"Characters: {len(document['content'])}")