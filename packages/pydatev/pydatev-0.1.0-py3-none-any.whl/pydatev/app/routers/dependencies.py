from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
import httpx

from ..config import settings

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.AUTH_URL,
    tokenUrl=settings.TOKEN_URL
)

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

# Add other client functions here... 