from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from typing import List
import httpx

from ..models.base import Client
from ..models.hr_files import JobInfo
from .dependencies import get_hr_files_client

router = APIRouter(prefix="/hr-files", tags=["HR Files"])

@router.post("/clients/{client_id}/files")
async def upload_hr_file(
    client_id: str,
    file: UploadFile = File(...),
    creation_time: str = Form(...),
    file_provider: str = Form(...),
    import_file_type: str = Form(...),
    payroll_accounting_month: str = Form(...),
    target_system: str = Form(...),
    client: httpx.AsyncClient = Depends(get_hr_files_client)
):
    """Upload a file for HR processing."""
    files = {"file": (file.filename, file.file, file.content_type)}
    data = {
        "creation_time": creation_time,
        "file_provider": file_provider,
        "import_file_type": import_file_type,
        "payroll_accounting_month": payroll_accounting_month,
        "target_system": target_system
    }
    
    response = await client.post(
        f"/v1/clients/{client_id}/files",
        files=files,
        data=data
    )
    if response.status_code == 201:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@router.get("/clients/{client_id}/jobs/{job_id}", response_model=JobInfo)
async def get_hr_file_job_status(
    client_id: str,
    job_id: str,
    client: httpx.AsyncClient = Depends(get_hr_files_client)
):
    """Get the status of a file upload job."""
    response = await client.get(f"/v1/clients/{client_id}/jobs/{job_id}")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@router.get("/clients", response_model=List[Client])
async def get_hr_files_clients(
    client: httpx.AsyncClient = Depends(get_hr_files_client)
):
    """Get list of clients with permission to use the HR files service."""
    response = await client.get("/v1/clients")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@router.get("/clients/{client_id}")
async def check_hr_files_permission(
    client_id: str,
    client: httpx.AsyncClient = Depends(get_hr_files_client)
):
    """Check if client has permission to use HR files service."""
    response = await client.get(f"/v1/clients/{client_id}")
    if response.status_code == 200:
        return {"has_permission": True}
    raise HTTPException(status_code=response.status_code, detail=response.text) 