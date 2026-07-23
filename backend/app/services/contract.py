import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.contract import ContractRepository
from app.schemas.contract import ContractCreate, ContractUpdate


class ContractService:
    def __init__(self, db: Session):
        self.repository = ContractRepository(db)

    def create_contract(self, contract_data: ContractCreate):
        return self.repository.create(contract_data)

    def get_contracts(self):
        return self.repository.get_all()

    def get_contract(self, contract_id: uuid.UUID):
        contract = self.repository.get_by_id(contract_id)

        if contract is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found",
            )

        return contract

    def update_contract(
        self,
        contract_id: uuid.UUID,
        contract_data: ContractUpdate,
    ):
        contract = self.get_contract(contract_id)

        return self.repository.update(
            contract,
            contract_data,
        )

    def delete_contract(self, contract_id: uuid.UUID):
        contract = self.get_contract(contract_id)

        self.repository.delete(contract)

        return {
            "message": "Contract deleted successfully",
        }