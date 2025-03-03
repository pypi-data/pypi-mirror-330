from fastapi import FastAPI, Depends, HTTPException, Header, File, UploadFile, Form
from fastapi.security import OAuth2AuthorizationCodeBearer
from typing import List, Optional, Dict, Any
import httpx

from .models import (
    Client, ClientWithServices, DocumentType, Document, 
    ProtocolEntry, ExtfJob, Tenant, CashRegisterMetadata, ClientsResponse, AppUpdate, SearchRequest, MasterClientFull,
    EauRequest, Feedback, SocialSecurityPayments, TaxPayments,
    Absences, JobInfo, DocumentMetadataDto, ClientWithAccessList
)
from .config import settings
from .routers import hr_eau, hr_exports, hr_files, hr_payroll

# Initialize FastAPI app
app = FastAPI(
    title="DATEV APIs Integration",
    description="Integration with DATEV APIs",
    version="2.0"
)

# OAuth2 configuration
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.AUTH_URL,
    tokenUrl=settings.TOKEN_URL
)

# API clients
async def get_docs_client(token: str = Depends(oauth2_scheme)):
    return httpx.AsyncClient(
        base_url=settings.ACCOUNTING_DOCS_API,
        headers={"Authorization": f"Bearer {token}"}
    )

async def get_dxso_client(token: str = Depends(oauth2_scheme)):
    return httpx.AsyncClient(
        base_url=settings.ACCOUNTING_DXSO_API,
        headers={"Authorization": f"Bearer {token}"}
    )

async def get_extf_client(token: str = Depends(oauth2_scheme)):
    return httpx.AsyncClient(
        base_url=settings.ACCOUNTING_EXTF_API,
        headers={"Authorization": f"Bearer {token}"}
    )

async def get_clients_client(token: str = Depends(oauth2_scheme)):
    return httpx.AsyncClient(
        base_url=settings.ACCOUNTING_CLIENTS_API,
        headers={"Authorization": f"Bearer {token}"}
    )

async def get_cash_register_client(token: str = Depends(oauth2_scheme)):
    return httpx.AsyncClient(
        base_url=settings.CASH_REGISTER_API,
        headers={"Authorization": f"Bearer {token}"}
    )

async def get_hr_client(token: str = Depends(oauth2_scheme)):
    return httpx.AsyncClient(
        base_url=settings.HR_DOCUMENTS_API,
        headers={"Authorization": f"Bearer {token}"}
    )

async def get_master_data_client(token: str = Depends(oauth2_scheme)):
    return httpx.AsyncClient(
        base_url=settings.MASTER_DATA_API,
        headers={"Authorization": f"Bearer {token}"}
    )

async def get_mytax_health_client(token: str = Depends(oauth2_scheme)):
    return httpx.AsyncClient(
        base_url=settings.MYTAX_HEALTH_API,
        headers={"Authorization": f"Bearer {token}"}
    )

# Add new client functions
async def get_eau_client(token: str = Depends(oauth2_scheme)):
    return httpx.AsyncClient(
        base_url=settings.HR_EAU_API,
        headers={"Authorization": f"Bearer {token}"}
    )

async def get_exports_client(token: str = Depends(oauth2_scheme)):
    return httpx.AsyncClient(
        base_url=settings.HR_EXPORTS_API,
        headers={"Authorization": f"Bearer {token}"}
    )

async def get_hr_files_client(token: str = Depends(oauth2_scheme)):
    return httpx.AsyncClient(
        base_url=settings.HR_FILES_API,
        headers={"Authorization": f"Bearer {token}"}
    )

async def get_payrollreports_client(token: str = Depends(oauth2_scheme)):
    return httpx.AsyncClient(
        base_url=settings.HR_PAYROLLREPORTS_API,
        headers={"Authorization": f"Bearer {token}"}
    )

# Accounting Clients API endpoints
@app.get("/clients", response_model=List[ClientWithServices])
async def get_clients(
    filter: Optional[str] = None,
    skip: Optional[int] = None,
    top: Optional[int] = None,
    client: httpx.AsyncClient = Depends(get_clients_client)
):
    """Get list of clients with their available services."""
    params = {"filter": filter, "skip": skip, "top": top}
    response = await client.get("/clients", params=params)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/clients/{client_id}", response_model=ClientWithServices)
async def get_client(
    client_id: str,
    client: httpx.AsyncClient = Depends(get_clients_client)
):
    """Get specific client details."""
    response = await client.get(f"/clients/{client_id}")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

# Accounting Documents API endpoints
@app.get("/clients/{client_id}/document-types", response_model=List[DocumentType])
async def get_document_types(
    client_id: str,
    client: httpx.AsyncClient = Depends(get_docs_client)
):
    """Get document types for a client."""
    response = await client.get(f"/clients/{client_id}/document-types")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.post("/clients/{client_id}/documents", response_model=Document)
async def upload_document(
    client_id: str,
    file: UploadFile = File(...),
    document_type: Optional[str] = Form(None),
    note: Optional[str] = Form(None),
    client: httpx.AsyncClient = Depends(get_docs_client)
):
    """Upload a document to DATEV."""
    files = {"file": (file.filename, file.file, file.content_type)}
    data = {}
    if document_type:
        data["document_type"] = document_type
    if note:
        data["note"] = note
    
    response = await client.post(
        f"/clients/{client_id}/documents",
        files=files,
        data=data
    )
    if response.status_code == 201:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

# DXSO Jobs API endpoints
@app.post("/clients/{client_id}/dxso-jobs", response_model=Dict[str, str])
async def create_dxso_job(
    client_id: str,
    client: httpx.AsyncClient = Depends(get_dxso_client)
):
    """Create a new DXSO job."""
    response = await client.post(f"/clients/{client_id}/dxso-jobs")
    if response.status_code == 201:
        return {"job_id": response.headers["Location"].split("/")[-1]}
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/clients/{client_id}/dxso-jobs/{job_id}/protocol", response_model=List[ProtocolEntry])
async def get_dxso_job_protocol(
    client_id: str,
    job_id: str,
    client: httpx.AsyncClient = Depends(get_dxso_client)
):
    """Get protocol entries for a DXSO job."""
    response = await client.get(f"/clients/{client_id}/dxso-jobs/{job_id}/protocol")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

# EXTF Files API endpoints
@app.post("/clients/{client_id}/extf-files/import")
async def import_extf_file(
    client_id: str,
    file: UploadFile = File(...),
    reference_id: Optional[str] = Header(None),
    client_application_version: Optional[str] = Header(None),
    client: httpx.AsyncClient = Depends(get_extf_client)
):
    """Import an EXTF file."""
    headers = {
        "Filename": file.filename,
        "Reference-Id": reference_id,
        "Client-Application-Version": client_application_version
    }
    
    response = await client.post(
        f"/clients/{client_id}/extf-files/import",
        content=await file.read(),
        headers=headers
    )
    if response.status_code == 202:
        return {
            "location": response.headers["Location"],
            "retry_after": response.headers["Retry-After"]
        }
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/clients/{client_id}/extf-files/jobs", response_model=List[ExtfJob])
async def get_extf_jobs(
    client_id: str,
    skip: Optional[int] = None,
    top: Optional[int] = None,
    client: httpx.AsyncClient = Depends(get_extf_client)
):
    """Get list of EXTF file import jobs."""
    params = {"skip": skip, "top": top}
    response = await client.get(f"/clients/{client_id}/extf-files/jobs", params=params)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

# Cash Register API endpoints
@app.get("/tenants", response_model=List[Tenant])
async def get_tenants(
    request_id: str = Header(...),
    client: httpx.AsyncClient = Depends(get_cash_register_client)
):
    """Get list of registered tenants."""
    response = await client.get(
        "/tenants",
        headers={"Request-Id": request_id}
    )
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.post("/tenants/{tenant_id}/files/import")
async def import_cash_register_file(
    tenant_id: str,
    file: UploadFile = File(...),
    metadata: CashRegisterMetadata = Form(...),
    request_id: str = Header(...),
    client: httpx.AsyncClient = Depends(get_cash_register_client)
):
    """Import file from cash-register to archive."""
    files = {
        "metadata": ("metadata.json", metadata.json(), "application/json"),
        "file": (file.filename, file.file, file.content_type)
    }
    
    response = await client.post(
        f"/tenants/{tenant_id}/files/import",
        files=files,
        headers={"Request-Id": request_id}
    )
    if response.status_code == 202:
        return {"message": "File accepted for processing"}
    raise HTTPException(status_code=response.status_code, detail=response.text)

# HR Documents API endpoints
@app.get("/hr/clients", response_model=ClientsResponse)
async def get_hr_clients(
    client: httpx.AsyncClient = Depends(get_hr_client)
):
    """Get list of HR clients."""
    response = await client.get("/clients")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.post("/hr/clients/{client_guid}/documents")
async def upload_hr_document(
    client_guid: str,
    file: UploadFile = File(...),
    client: httpx.AsyncClient = Depends(get_hr_client)
):
    """Upload document to DATEV Personalakte."""
    files = {"file": (file.filename, file.file, file.content_type)}
    response = await client.post(
        f"/clients/{client_guid}/documents",
        files=files
    )
    if response.status_code == 200:
        return {"message": "Document uploaded successfully"}
    raise HTTPException(status_code=response.status_code, detail=response.text)

# Master Data API endpoints
@app.put("/apps", response_model=Dict[str, Any])
async def update_app(
    app_update: AppUpdate,
    client: httpx.AsyncClient = Depends(get_master_data_client)
):
    """Update app configuration."""
    response = await client.put("/apps", json=app_update.dict())
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.post("/master-clients/search", response_model=List[MasterClientFull])
async def search_master_clients(
    search_request: SearchRequest,
    expand: Optional[str] = None,
    client: httpx.AsyncClient = Depends(get_master_data_client)
):
    """Search for master clients."""
    params = {"expand": expand} if expand else None
    response = await client.post(
        "/master-clients/search",
        json=search_request.dict(exclude_none=True),
        params=params
    )
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

# MyTax Income Tax Documents Health API endpoint
@app.get("/health")
async def check_health(
    client: httpx.AsyncClient = Depends(get_mytax_health_client)
):
    """Check health status of the service."""
    response = await client.get("/actuator/health")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

# HR eAU API endpoints
@app.post("/clients/{consultant_number}-{client_number}/employees/{personnel_number}/eau-requests", response_model=Dict[str, str])
async def create_eau_request(
    consultant_number: str,
    client_number: str,
    personnel_number: str,
    eau_request: EauRequest,
    client: httpx.AsyncClient = Depends(get_eau_client)
):
    """Create a new eAU request."""
    response = await client.post(
        f"/clients/{consultant_number}-{client_number}/employees/{personnel_number}/eau-requests",
        json=eau_request.dict()
    )
    if response.status_code == 201:
        return {"location": response.headers["Location"]}
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/clients/{consultant_number}-{client_number}/employees/{personnel_number}/eau-requests/{eau_request}/feedbacks", response_model=Feedback)
async def get_eau_feedbacks(
    consultant_number: str,
    client_number: str,
    personnel_number: str,
    eau_request: str,
    client: httpx.AsyncClient = Depends(get_eau_client)
):
    """Get feedbacks for an eAU request."""
    response = await client.get(
        f"/clients/{consultant_number}-{client_number}/employees/{personnel_number}/eau-requests/{eau_request}/feedbacks"
    )
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

# Additional HR eAU API endpoints
@app.delete("/clients/{consultant_number}-{client_number}/employees/{personnel_number}/eau-requests/{eau_request}")
async def cancel_eau_request(
    consultant_number: str,
    client_number: str,
    personnel_number: str,
    eau_request: str,
    client: httpx.AsyncClient = Depends(get_eau_client)
):
    """Cancel an eAU request."""
    response = await client.delete(
        f"/clients/{consultant_number}-{client_number}/employees/{personnel_number}/eau-requests/{eau_request}"
    )
    if response.status_code == 204:
        return {"message": "Request successfully cancelled"}
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/clients/{consultant_number}-{client_number}")
async def check_eau_permission(
    consultant_number: str,
    client_number: str,
    client: httpx.AsyncClient = Depends(get_eau_client)
):
    """Check if client has permission to use eAU-API."""
    response = await client.get(f"/clients/{consultant_number}-{client_number}")
    if response.status_code == 200:
        return {"has_permission": True}
    raise HTTPException(status_code=response.status_code, detail=response.text)

# HR Exports API endpoints
@app.get("/exports/clients/{client_id}/employees/{employee_id}/socialsecurity", response_model=SocialSecurityPayments)
async def get_social_security_payments(
    client_id: str,
    employee_id: int,
    payroll_accounting_month: str,
    client: httpx.AsyncClient = Depends(get_exports_client)
):
    """Get social security payments for an employee."""
    response = await client.get(
        f"/clients/{client_id}/employees/{employee_id}/socialsecurity",
        params={"payroll_accounting_month": payroll_accounting_month}
    )
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/exports/clients/{client_id}/employees/{employee_id}/taxpayments", response_model=TaxPayments)
async def get_tax_payments(
    client_id: str,
    employee_id: int,
    payroll_accounting_month: str,
    client: httpx.AsyncClient = Depends(get_exports_client)
):
    """Get tax payments for an employee."""
    response = await client.get(
        f"/clients/{client_id}/employees/{employee_id}/taxpayments",
        params={"payroll_accounting_month": payroll_accounting_month}
    )
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/exports/clients/{client_id}/employees/{employee_id}/absences", response_model=Absences)
async def get_employee_absences(
    client_id: str,
    employee_id: int,
    payroll_accounting_month: str,
    client: httpx.AsyncClient = Depends(get_exports_client)
):
    """Get absences for an employee."""
    response = await client.get(
        f"/clients/{client_id}/employees/{employee_id}/absences",
        params={"payroll_accounting_month": payroll_accounting_month}
    )
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

# HR Files API endpoints
@app.post("/hr-files/clients/{client_id}/files")
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

@app.get("/hr-files/clients/{client_id}/jobs/{job_id}", response_model=JobInfo)
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

@app.get("/hr-files/clients", response_model=List[Client])
async def get_hr_files_clients(
    client: httpx.AsyncClient = Depends(get_hr_files_client)
):
    """Get list of clients with permission to use the HR files service."""
    response = await client.get("/v1/clients")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/hr-files/clients/{client_id}")
async def check_hr_files_permission(
    client_id: str,
    client: httpx.AsyncClient = Depends(get_hr_files_client)
):
    """Check if client has permission to use HR files service."""
    response = await client.get(f"/v1/clients/{client_id}")
    if response.status_code == 200:
        return {"has_permission": True}
    raise HTTPException(status_code=response.status_code, detail=response.text)

# HR Payroll Reports API endpoints
@app.get("/payrollreports/clients/{client_id}/documents/{period}", response_model=List[Dict[str, Any]])
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

@app.get("/payrollreports/clients/{client_id}/documents-metadata", response_model=DocumentMetadataDto)
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

@app.get("/payrollreports/clients/{client_id}/documents/{period}/status")
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

@app.get("/payrollreports/clients", response_model=List[Client])
async def get_payroll_clients(
    client: httpx.AsyncClient = Depends(get_payrollreports_client)
):
    """Get list of clients with access to payroll reports."""
    response = await client.get("/clients")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/payrollreports/clients/{client_id}", response_model=ClientWithAccessList)
async def get_payroll_client_access(
    client_id: str,
    client: httpx.AsyncClient = Depends(get_payrollreports_client)
):
    """Get client with list of accessible document types."""
    response = await client.get(f"/clients/{client_id}")
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.text)

# Include routers
app.include_router(hr_eau.router)
app.include_router(hr_exports.router)
app.include_router(hr_files.router)
app.include_router(hr_payroll.router) 