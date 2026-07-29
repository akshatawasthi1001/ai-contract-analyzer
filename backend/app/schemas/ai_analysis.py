from pydantic import BaseModel, Field


class KeyClause(BaseModel):
    title: str
    description: str
    importance: str


class ContractRisk(BaseModel):
    title: str
    description: str
    severity: str


class ContractObligation(BaseModel):
    party: str
    obligation: str
    description: str


class ContractObservation(BaseModel):
    title: str
    description: str


class ContractAnalysisResponse(BaseModel):
    summary: str
    key_clauses: list[KeyClause] = Field(default_factory=list)
    obligations: list[ContractObligation] = Field(default_factory=list)
    risks: list[ContractRisk] = Field(default_factory=list)
    observations: list[ContractObservation] = Field(
        default_factory=list
    )