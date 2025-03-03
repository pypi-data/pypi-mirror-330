from pydantic import BaseModel

class JobInfo(BaseModel):
    job_id: str
    timestamp: str
    state: str 