from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
import httpx

from ..models.hr_eau import EauRequest, Feedback
from ..config import settings
from .dependencies import get_eau_client

router = APIRouter(prefix="/eau", tags=["HR eAU"])

@router.post("/clients/{consultant_number}-{client_number}/employees/{personnel_number}/eau-requests", response_model=Dict[str, str])
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

@router.get("/clients/{consultant_number}-{client_number}/employees/{personnel_number}/eau-requests/{eau_request}/feedbacks", response_model=Feedback)
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

@router.delete("/clients/{consultant_number}-{client_number}/employees/{personnel_number}/eau-requests/{eau_request}")
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

@router.get("/clients/{consultant_number}-{client_number}")
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