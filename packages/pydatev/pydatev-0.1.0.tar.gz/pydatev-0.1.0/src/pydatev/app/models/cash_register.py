from pydantic import BaseModel
from datetime import datetime

class CashRegisterMetadata(BaseModel):
    tenant_id: str
    creation_date: datetime
    file_type: str
    source_system: str 