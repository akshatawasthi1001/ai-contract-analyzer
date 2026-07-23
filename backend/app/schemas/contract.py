import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.contract import ContractStatus


class ContractCreate(BaseModel):
    title: str
    description: str | None = None


class ContractUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class ContractResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str | None
    status: ContractStatus
    created_at: datetime
    updated_at: datetime