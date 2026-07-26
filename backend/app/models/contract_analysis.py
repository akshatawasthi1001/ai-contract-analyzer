import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ContractAnalysis(Base):
    __tablename__ = "contract_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    contract_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    key_clauses: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    obligations: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    risks: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    observations: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    model_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="llama3.2",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    contract = relationship(
        "Contract",
        back_populates="analysis",
    )