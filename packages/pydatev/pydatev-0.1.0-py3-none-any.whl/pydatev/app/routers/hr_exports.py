from fastapi import APIRouter, Depends, HTTPException
import httpx

from ..models.hr_exports import SocialSecurityPayments, TaxPayments, Absences
from .dependencies import get_exports_client

router = APIRouter(prefix="/exports", tags=["HR Exports"])

@router.get("/clients/{client_id}/employees/{employee_id}/socialsecurity", response_model=SocialSecurityPayments)
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

@router.get("/clients/{client_id}/employees/{employee_id}/taxpayments", response_model=TaxPayments)
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

@router.get("/clients/{client_id}/employees/{employee_id}/absences", response_model=Absences)
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