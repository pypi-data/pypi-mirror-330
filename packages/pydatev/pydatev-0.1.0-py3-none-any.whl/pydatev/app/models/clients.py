from pydantic import BaseModel
from typing import List
from .base import Client

class ClientsResponse(BaseModel):
    clients: List[Client]
    total_count: int

class ClientWithAccessList(Client):
    accessible_document_types: List[str] 