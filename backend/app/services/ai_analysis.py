import json

from ollama import Client
from pydantic import ValidationError

from app.schemas.ai_analysis import ContractAnalysisResponse


class AIAnalysisService:

    def __init__(
        self,
        model: str = "llama3.2:latest",
    ):
        self.model = model

        # Ollama is running on the Windows host.
        # Backend is running inside Docker.
        self.client = Client(
            host="http://host.docker.internal:11434"
        )

    def analyze_contract(
        self,
        contract_text: str,
    ) -> ContractAnalysisResponse:

        if not contract_text.strip():
            raise ValueError(
                "Contract text cannot be empty."
            )

        prompt = self._build_prompt(
            contract_text
        )

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI contract analysis assistant. "
                        "Analyze contracts carefully. "
                        "Return only valid JSON matching the requested structure."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            format="json",
        )

        content = response["message"]["content"]

        try:
            parsed_response = json.loads(content)

            return ContractAnalysisResponse.model_validate(
                parsed_response
            )

        except (
            json.JSONDecodeError,
            ValidationError,
        ) as exc:
            raise ValueError(
                "AI returned an invalid contract analysis response."
            ) from exc

    @staticmethod
    def _build_prompt(
        contract_text: str,
    ) -> str:

        return f"""
Analyze the following document as a legal contract.

Return ONLY valid JSON using exactly this structure:

{{
    "summary": "A concise summary of the contract.",
    "key_clauses": [
        {{
            "title": "Clause title",
            "description": "What the clause says.",
            "importance": "Why this clause is important."
        }}
    ],
    "obligations": [
        {{
            "party": "Party responsible.",
            "obligation": "What the party must do.",
            "description": "Detailed explanation of the obligation."
        }}
    ],
    "risks": [
        {{
            "title": "Risk title.",
            "description": "Description of the potential risk.",
            "severity": "low"
        }}
    ],
    "observations": [
        {{
            "title": "Observation title.",
            "description": "Important observation."
        }}
    ]
}}

Rules:
- Return only valid JSON.
- Do not include Markdown.
- Do not wrap the JSON in code blocks.
- Do not add any text before or after the JSON.
- Do not invent facts.
- Base the analysis only on the provided document.
- If information is unavailable, use an empty list.
- If the document does not appear to be a legal contract,
  clearly state this in the summary.
- For risks, severity must be one of: "low", "medium", or "high".

Contract:
--------------------
{contract_text}
--------------------
"""