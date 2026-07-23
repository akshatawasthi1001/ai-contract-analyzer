import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.contract import (
    ContractCreate,
    ContractResponse,
    ContractUpdate,
)
from app.services.contract import ContractService


router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"],
)


@router.post(
    "",
    response_model=ContractResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contract(
    contract_data: ContractCreate,
    db: Session = Depends(get_db),
):
    service = ContractService(db)

    return service.create_contract(contract_data)


@router.get(
    "",
    response_model=list[ContractResponse],
)
def get_contracts(
    db: Session = Depends(get_db),
):
    service = ContractService(db)

    return service.get_contracts()


@router.get(
    "/{contract_id}",
    response_model=ContractResponse,
)
def get_contract(
    contract_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    service = ContractService(db)

    return service.get_contract(contract_id)


@router.patch(
    "/{contract_id}",
    response_model=ContractResponse,
)
def update_contract(
    contract_id: uuid.UUID,
    contract_data: ContractUpdate,
    db: Session = Depends(get_db),
):
    service = ContractService(db)

    return service.update_contract(
        contract_id,
        contract_data,
    )


@router.delete(
    "/{contract_id}",
)
def delete_contract(
    contract_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    service = ContractService(db)

    return service.delete_contract(contract_id)