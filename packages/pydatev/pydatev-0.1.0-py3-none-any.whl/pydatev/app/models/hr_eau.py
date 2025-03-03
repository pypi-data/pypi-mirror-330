from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import date

class EauRequest(BaseModel):
    start_date: date
    end_date: date
    reason: str
    notes: Optional[str]

class Feedback(BaseModel):
    status: str
    message: str
    timestamp: date

# Your HR EAU models here 