import ollama


def analyze_contract(text: str) -> str:
    prompt = f"""
You are an AI legal contract analysis assistant.

Analyze the following document and provide a clear, structured analysis.

Return the following sections:

1. Summary
2. Key Clauses
3. Obligations
4. Potential Risks
5. Important Observations

If the uploaded document does not appear to be a legal contract,
clearly state that it may not be a legal contract.

Document:

{text}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]