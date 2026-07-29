from sqlalchemy.orm import Session

from app.models.contract_analysis import ContractAnalysis


class ContractAnalysisService:

    @staticmethod
    def create_analysis(
        db: Session,
        contract_id,
        summary: str,
        key_clauses: list,
        obligations: list,
        risks: list,
        observations: list,
        model_name: str = "llama3.2",
    ) -> ContractAnalysis:

        analysis = ContractAnalysis(
            contract_id=contract_id,
            summary=summary,
            key_clauses=key_clauses,
            obligations=obligations,
            risks=risks,
            observations=observations,
            model_name=model_name,
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return analysis

    @staticmethod
    def get_analysis(
        db: Session,
        contract_id,
    ) -> ContractAnalysis | None:

        return (
            db.query(ContractAnalysis)
            .filter(
                ContractAnalysis.contract_id == contract_id
            )
            .order_by(
                ContractAnalysis.created_at.desc()
            )
            .first()
        )