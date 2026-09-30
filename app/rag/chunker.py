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
    Split a large section into smaller chunks while preserving
    paragraph structure as much as possible, applying a character overlap.
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

        # Handle edge case: single paragraph exceeds max_chunk_size
        if len(paragraph) > max_chunk_size:
            # First, flush whatever was accumulating
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            # Hard-split the oversized paragraph with overlap
            start = 0
            para_len = len(paragraph)
            while start < para_len:
                end = start + max_chunk_size
                chunk_str = paragraph[start:end]

                # Try to break at a space near the end to avoid splitting words
                if end < para_len:
                    last_space = chunk_str.rfind(" ")
                    if last_space > max_chunk_size - chunk_overlap:
                        end = start + last_space

                chunks.append(paragraph[start:end].strip())
                start = end - chunk_overlap if end < para_len else para_len

            continue

        # Check if adding paragraph exceeds max_chunk_size
        if not current_chunk:
            current_chunk = paragraph
        elif len(current_chunk) + len(paragraph) + 2 <= max_chunk_size:
            current_chunk += "\n\n" + paragraph
        else:
            chunks.append(current_chunk.strip())

            # Create overlap context from the tail of current_chunk
            overlap_text = current_chunk[-chunk_overlap:].strip() if chunk_overlap > 0 else ""
            
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
    Split Markdown content primarily by headings.

    Each Markdown section is kept together when possible.
    Large sections are further split by paragraph boundaries with overlap.
    """
    text = text.strip()

    if not text:
        return []

    # Match Markdown headings (# Title, ## Section, etc.)
    heading_pattern = r"(?m)^#{1,6}\s+.+$"

    matches = list(re.finditer(heading_pattern, text))

    if not matches:
        return split_large_text(
            text,
            max_chunk_size=max_chunk_size,
            chunk_overlap=chunk_overlap,
        )

    sections = []

    # Preserve content before the first heading
    if matches[0].start() > 0:
        preamble = text[: matches[0].start()].strip()
        if preamble:
            sections.extend(
                split_large_text(
                    preamble,
                    max_chunk_size=max_chunk_size,
                    chunk_overlap=chunk_overlap,
                )
            )

    for index, match in enumerate(matches):
        start = match.start()
        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(text)

        section = text[start:end].strip()

        if not section:
            continue

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

    for chunk in chunks[:10]:
        print("\n-----------------------------")
        print(f"Source: {chunk['metadata']['source']}")
        print(f"Chunk index: {chunk['metadata']['chunk_index']}")
        print(f"Total chunks in document: {chunk['metadata']['total_chunks']}")
        print(f"Characters: {len(chunk['content'])}")
        print("\nContent:")
        print(chunk["content"])