from pydantic import BaseModel
from typing import Dict, List, Any

class DocumentMetadataDto(BaseModel):
    employee_documents: List[Dict[str, Any]]
    client_documents: List[Dict[str, Any]]

class ClientWithAccessList(BaseModel):
    client_id: str
    consultant_number: int
    client_number: int
    document_types: Dict[str, List[str]] 