import pandas as pd

from app.rag.retriever import search_documents
from app.rag.embedder import load_embedding_model


EVALUATION_FILE = "evaluation/rag_evaluation.csv"

model = load_embedding_model()

def calculate_reciprocal_rank(
    retrieved_documents,
    expected_document,
):
    """
    Calculate the reciprocal rank of the expected document.

    If the expected document is not retrieved, return 0.
    """
    for rank, document in enumerate(
        retrieved_documents,
        start=1,
    ):
        if document == expected_document:
            return 1 / rank

    return 0.0


def evaluate_retrieval(top_k: int = 3):
    """
    Evaluate document-level retrieval performance.

    Metrics:
    - Recall@1
    - Recall@3 (or the supplied top_k)
    - MRR
    """

    evaluation_data = pd.read_csv(EVALUATION_FILE)

    total_questions = len(evaluation_data)

    recall_at_1_hits = 0
    recall_at_k_hits = 0
    reciprocal_ranks = []

    print("\n" + "=" * 70)
    print("RAG RETRIEVAL EVALUATION")
    print("=" * 70)

    for index, row in evaluation_data.iterrows():

        question = row["question"]
        expected_document = row["expected_document"]

        results = search_documents(
            query=question,
            top_k=top_k,
            model = model
        )

        retrieved_documents = [
            metadata["source"]
            for metadata in results["metadatas"][0]
        ]

        # Find the rank of the first occurrence of the expected document.
        expected_rank = None

        for rank, document in enumerate(
            retrieved_documents,
            start=1,
        ):
            if document == expected_document:
                expected_rank = rank
                break

        # Recall@1
        if expected_rank == 1:
            recall_at_1_hits += 1

        # Recall@K
        if expected_rank is not None:
            recall_at_k_hits += 1

        # Reciprocal Rank for MRR
        reciprocal_rank = calculate_reciprocal_rank(
            retrieved_documents=retrieved_documents,
            expected_document=expected_document,
        )

        reciprocal_ranks.append(reciprocal_rank)

        print("\n" + "-" * 70)
        print(f"Question: {question}")
        print(f"Expected: {expected_document}")

        print("\nRetrieved:")

        for rank, document in enumerate(
            retrieved_documents,
            start=1,
        ):
            marker = ""

            if document == expected_document:
                marker = " <-- expected"

            print(
                f"{rank}. {document}{marker}"
            )

        print(
            f"Expected document rank: "
            f"{expected_rank if expected_rank is not None else 'Not found'}"
        )

        print(
            f"Reciprocal rank: "
            f"{reciprocal_rank:.3f}"
        )

    recall_at_1 = recall_at_1_hits / total_questions
    recall_at_k = recall_at_k_hits / total_questions
    mrr = sum(reciprocal_ranks) / total_questions

    print("\n" + "=" * 70)
    print("FINAL METRICS")
    print("=" * 70)

    print(
        f"Total questions: {total_questions}"
    )

    print(
        f"Recall@1: {recall_at_1:.3f} "
        f"({recall_at_1_hits}/{total_questions})"
    )

    print(
        f"Recall@{top_k}: {recall_at_k:.3f} "
        f"({recall_at_k_hits}/{total_questions})"
    )

    print(
        f"MRR: {mrr:.3f}"
    )

    print("=" * 70)


if __name__ == "__main__":
    evaluate_retrieval(top_k=3)
