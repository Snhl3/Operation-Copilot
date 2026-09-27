from app.rag.retriever import search_documents
from app.rag.generator import generate_answer


def build_context(results):
    """
    Combine retrieved document chunks into
    a single context string.
    """

    documents = results["documents"][0]

    context_parts = []

    for index, document in enumerate(documents):
        context_parts.append(
            f"[Context {index + 1}]\n{document}"
        )

    return "\n\n".join(context_parts)


def answer_question(
    question: str,
    top_k: int = 3,
):
    """
    Complete basic RAG pipeline:

    Question
        ↓
    Retrieval
        ↓
    Context
        ↓
    LLM
        ↓
    Answer
    """

    results = search_documents(
        query=question,
        top_k=top_k,
    )

    context = build_context(results)

    answer = generate_answer(
        question=question,
        context=context,
    )

    sources = []

    for metadata in results["metadatas"][0]:
        sources.append(
            {
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
            }
        )

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }


if __name__ == "__main__":

    question = (
        "What should I check before starting production?"
    )

    result = answer_question(
        question=question,
        top_k=3,
    )

    print("\nQuestion:")
    print(result["question"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(
            f"- {source['source']} "
            f"(chunk {source['chunk_index']})"
        )