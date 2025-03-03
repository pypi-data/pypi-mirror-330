from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobInfo(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    error_message: Optional[str] 