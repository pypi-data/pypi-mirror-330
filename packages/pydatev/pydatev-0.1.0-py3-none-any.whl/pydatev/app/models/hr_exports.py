from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class SocialSecurityPayments(BaseModel):
    employee_id: int
    month: str
    amount: float
    insurance_type: str

class TaxPayments(BaseModel):
    employee_id: int
    month: str
    tax_amount: float
    tax_type: str

class Absences(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    type: str
    reason: Optional[str] 