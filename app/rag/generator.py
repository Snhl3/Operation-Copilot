import ollama


MODEL_NAME = "qwen3:1.7b"


def generate_answer(
    question: str,
    context: str,
) -> str:
    """
    Generate an answer using the retrieved context.
    """

    prompt = f"""
You are an Industrial AI Operations Copilot.

Answer the user's question using ONLY the provided
industrial documentation context.

Rules:
- Do not use outside knowledge.
- Do not invent information.
- If the answer is not present in the context,
  say that the information is not available in the
  provided documentation.
- Keep the answer concise.
- Use bullet points when appropriate.
- Do not discuss topics outside the provided context.

Industrial documentation context:
-------------------------
{context}
-------------------------

User question:
{question}

Answer:
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        think=False,
    )

    return response["message"]["content"]


if __name__ == "__main__":

    question = (
        "What should I check before "
        "starting production?"
    )

    context = """
Before starting production, operators should verify
equipment condition, safety guards, emergency stops,
lubrication status, tool condition, and operating
parameters.
"""

    answer = generate_answer(
        question=question,
        context=context,
    )

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)