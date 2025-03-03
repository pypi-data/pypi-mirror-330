from pydantic import BaseModel
from typing import Optional

class Tenant(BaseModel):
    id: str
    name: str
    tax_number: Optional[str]
    tax_consultant_number: Optional[str] 