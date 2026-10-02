
import re

from app.rag.loader import load_documents

MAX_CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def split_large_text(
    text: str,
    max_chunk_size: int = MAX_CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """
    Split a large section into smaller chunks while
    preserving paragraph structure as much as possible.
    Apply character overlap when a section is split.
    """
    text = text.strip()

    if not text:
        return []

    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    paragraphs = re.split(r"\n\s*\n", text)
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # Handle a paragraph larger than the chunk limit.
        if len(paragraph) > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            start = 0
            para_len = len(paragraph)

            while start < para_len:
                end = min(start + max_chunk_size, para_len)

                # Try to split at a space near the end.
                if end < para_len:
                    chunk_str = paragraph[start:end]
                    last_space = chunk_str.rfind(" ")

                    if last_space > max_chunk_size - chunk_overlap:
                        end = start + last_space

                chunks.append(paragraph[start:end].strip())

                if end >= para_len:
                    break

                start = max(0, end - chunk_overlap)

            continue

        # Add paragraph if it fits.
        if not current_chunk:
            current_chunk = paragraph

        elif len(current_chunk) + len(paragraph) + 2 <= max_chunk_size:
            current_chunk += "\n\n" + paragraph

        else:
            chunks.append(current_chunk.strip())

            # Carry a small amount of context forward.
            overlap_text = (
                current_chunk[-chunk_overlap:].strip()
                if chunk_overlap > 0
                else ""
            )

            if overlap_text:
                current_chunk = overlap_text + "\n\n" + paragraph
            else:
                current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def split_markdown_sections(
    text: str,
    max_chunk_size: int = MAX_CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """
    Split Markdown by section headings (## to ######).

    A top-level document title (#) is retained as context
    and attached to the first meaningful section.

    Large sections are further split by paragraphs.
    """
    text = text.strip()

    if not text:
        return []

    # Split on section headings, not the document title.
    heading_pattern = r"(?m)^#{2,6}\s+.+$"
    matches = list(re.finditer(heading_pattern, text))

    # If there are no section headings, split the
    # complete document by paragraph structure.
    if not matches:
        return split_large_text(
            text,
            max_chunk_size=max_chunk_size,
            chunk_overlap=chunk_overlap,
        )

    sections = []

    # Content before the first section heading.
    # This usually contains the document title.
    preamble = text[:matches[0].start()].strip()

    for index, match in enumerate(matches):
        start = match.start()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(text)

        section = text[start:end].strip()

        if not section:
            continue

        # Attach the title/preamble to the first
        # meaningful section instead of making
        # it a standalone retrieval chunk.
        if index == 0 and preamble:
            section = preamble + "\n\n" + section

        sections.extend(
            split_large_text(
                section,
                max_chunk_size=max_chunk_size,
                chunk_overlap=chunk_overlap,
            )
        )

    return sections


def create_chunks(documents):
    """
    Create structure-aware chunks from Markdown documents.
    """
    chunks = []

    for document in documents:
        document_chunks = split_markdown_sections(
            document["content"],
            max_chunk_size=MAX_CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

        for chunk_index, chunk_text in enumerate(document_chunks):
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


if __name__ == "__main__":
    documents = load_documents()
    chunks = create_chunks(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")

    for chunk in chunks:
        print("\n" + "=" * 70)
        print(f"Source: {chunk['metadata']['source']}")
        print(f"Chunk index: {chunk['metadata']['chunk_index']}")
        print(f"Total chunks: {chunk['metadata']['total_chunks']}")
        print(f"Characters: {len(chunk['content'])}")
        print("\nContent:")
        print(chunk["content"])