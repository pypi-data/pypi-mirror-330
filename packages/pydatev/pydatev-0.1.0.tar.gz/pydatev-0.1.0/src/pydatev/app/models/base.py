from pydantic import BaseModel
from typing import List, Optional

class Service(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class Client(BaseModel):
    id: str
    name: str
    number: str
    consultant_number: Optional[str] = None

class ClientWithServices(Client):
    services: List[Service] 