import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate


class ContractRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, contract_data: ContractCreate) -> Contract:
        contract = Contract(
            title=contract_data.title,
            description=contract_data.description,
        )

        self.db.add(contract)
        self.db.commit()
        self.db.refresh(contract)

        return contract

    def get_all(self) -> list[Contract]:
        statement = select(Contract).order_by(Contract.created_at.desc())
        return list(self.db.scalars(statement).all())

    def get_by_id(self, contract_id: uuid.UUID) -> Contract | None:
        statement = select(Contract).where(Contract.id == contract_id)
        return self.db.scalar(statement)

    def update(
        self,
        contract: Contract,
        contract_data: ContractUpdate,
    ) -> Contract:
        if contract_data.title is not None:
            contract.title = contract_data.title

        if contract_data.description is not None:
            contract.description = contract_data.description

        self.db.commit()
        self.db.refresh(contract)

        return contract

    def delete(self, contract: Contract) -> None:
        self.db.delete(contract)
        self.db.commit()