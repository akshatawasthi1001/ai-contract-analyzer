import uuid
from pathlib import Path

import fitz
from docx import Document
from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.contract import (
    ContractCreate,
    ContractResponse,
    ContractUpdate,
)
from app.services.ai_analysis import analyze_contract
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


@router.post(
    "/{contract_id}/upload",
    status_code=status.HTTP_200_OK,
)
async def upload_contract_file(
    contract_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Allowed file types
    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    # Validate file type
    if file.content_type not in allowed_types:
        return {
            "error": "Only PDF and DOCX files are supported."
        }

    # Create storage directory
    storage_dir = Path("storage/contracts")
    storage_dir.mkdir(parents=True, exist_ok=True)

    # Create unique file path
    file_path = storage_dir / f"{contract_id}_{file.filename}"

    # Save uploaded file
    file_content = await file.read()
    file_path.write_bytes(file_content)

    # Extract text
    extracted_text = ""

    # PDF text extraction
    if file.content_type == "application/pdf":
        pdf_document = fitz.open(file_path)

        for page in pdf_document:
            extracted_text += page.get_text()

        pdf_document.close()

    # DOCX text extraction
    elif (
        file.content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        document = Document(file_path)

        extracted_text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    return {
        "contract_id": str(contract_id),
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File uploaded and text extracted successfully",
        "text": extracted_text,
    }

@router.post(
    "/{contract_id}/analyze",
    status_code=status.HTTP_200_OK,
)
def analyze_contract_document(
    contract_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    # Get the contract file path
    storage_dir = Path("storage/contracts")

    matching_files = list(
        storage_dir.glob(f"{contract_id}_*")
    )

    if not matching_files:
        return {
            "error": "Contract file not found. Please upload the contract first."
        }

    file_path = matching_files[0]

    # Extract text from the saved file
    extracted_text = ""

    if file_path.suffix.lower() == ".pdf":
        pdf_document = fitz.open(file_path)

        for page in pdf_document:
            extracted_text += page.get_text()

        pdf_document.close()

    elif file_path.suffix.lower() == ".docx":
        document = Document(file_path)

        extracted_text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    else:
        return {
            "error": "Unsupported file format."
        }

    # Send extracted text to OpenAI
    ai_analysis = analyze_contract(extracted_text)

    return {
        "contract_id": str(contract_id),
        "filename": file_path.name,
        "message": "Contract analyzed successfully",
        "analysis": ai_analysis,
    }