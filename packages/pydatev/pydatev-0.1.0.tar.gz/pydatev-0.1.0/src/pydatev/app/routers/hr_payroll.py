from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
import httpx

from ..models.base import Client
from ..models.hr_payroll import DocumentMetadataDto, ClientWithAccessList
from .dependencies import get_payrollreports_client

router = APIRouter(prefix="/payrollreports", tags=["HR Payroll Reports"])

@router.get("/clients/{client_id}/documents/{period}", response_model=List[Dict[str, Any]])
async def get_payroll_documents(
    client_id: str,
    period: str,
    document_types: List[str],
    employee_number: Optional[int] = None,
    client: httpx.AsyncClient = Depends(get_payrollreports_client)
):
    """Get payroll documents for a period."""
    params = {
        "document_types": document_types,
        "employee_number": employee_number
    }
    
    response = await client.get(
        f"/clients/{client_id}/documents/{period}",
        params=params,
        headers={"Accept": "application/pdf"}
    )
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@router.get("/clients/{client_id}/documents-metadata", response_model=DocumentMetadataDto)
async def get_documents_metadata(
    client_id: str,
    document_types: str,
    period: Optional[str] = None,
    timestamp: Optional[str] = None,
    client: httpx.AsyncClient = Depends(get_payrollreports_client)
):
    """Get metadata for payroll documents."""
    params = {
        "document_types": document_types,
        "period": period,
        "timestamp": timestamp
    }
    
    response = await client.get(
        f"/clients/{client_id}/documents-metadata",
        params=params
    )
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@router.get("/clients/{client_id}/documents/{period}/status")
async def check_documents_status(
    client_id: str,
    period: str,
    client: httpx.AsyncClient = Depends(get_payrollreports_client)
):
    """Check if documents exist for the given period."""
    response = await client.get(f"/clients/{client_id}/documents/{period}/status")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@router.get("/clients", response_model=List[Client])
async def get_payroll_clients(
    client: httpx.AsyncClient = Depends(get_payrollreports_client)
):
    """Get list of clients with access to payroll reports."""
    response = await client.get("/clients")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@router.get("/clients/{client_id}", response_model=ClientWithAccessList)
async def get_payroll_client_access(
    client_id: str,
    client: httpx.AsyncClient = Depends(get_payrollreports_client)
):
    """Get client with list of accessible document types."""
    response = await client.get(f"/clients/{client_id}")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text) 