from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProtocolEntry(BaseModel):
    timestamp: datetime
    message: str
    severity: str

class ExtfJob(BaseModel):
    id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    protocol: List[ProtocolEntry] 