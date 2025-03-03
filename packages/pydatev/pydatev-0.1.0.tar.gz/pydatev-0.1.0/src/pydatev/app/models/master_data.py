from pydantic import BaseModel
from typing import Optional, Dict, Any

class AppUpdate(BaseModel):
    app_id: str
    version: str
    settings: Dict[str, Any]

class SearchRequest(BaseModel):
    search_term: str
    max_results: Optional[int] = 10

class MasterClientFull(BaseModel):
    id: str
    name: str
    number: str
    tax_number: Optional[str]
    address: Optional[Dict[str, str]] 