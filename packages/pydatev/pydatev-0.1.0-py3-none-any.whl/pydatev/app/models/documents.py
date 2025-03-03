from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentType(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class Document(BaseModel):
    id: str
    filename: str
    document_type: Optional[str]
    upload_date: datetime
    note: Optional[str] = None

class DocumentMetadataDto(BaseModel):
    document_id: str
    document_types: List[str]
    period: Optional[str]
    timestamp: datetime 