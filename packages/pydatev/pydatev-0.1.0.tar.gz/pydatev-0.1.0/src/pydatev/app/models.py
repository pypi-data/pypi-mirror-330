from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Common models
class Client(BaseModel):
    client_number: int
    consultant_number: int
    id: str
    name: str

class Service(BaseModel):
    name: str
    scopes: List[str]

class ClientWithServices(Client):
    services: List[Service]

# Accounting Documents models
class Ledgers(BaseModel):
    is_accounts_payable_ledger_available: bool
    is_accounts_receivable_ledger_available: bool
    is_cash_ledger_available: bool

class BasicAccountingInformation(BaseModel):
    fiscal_year_start: datetime
    fiscal_year_end: datetime
    account_length: int
    datev_chart_of_accounts: Optional[int]
    ledgers: Ledgers

class ClientBasics(Client):
    is_document_management_available: bool
    basic_accounting_information: List[BasicAccountingInformation]

class DocumentType(BaseModel):
    name: str
    category: str
    debit_credit_identifier: Optional[str]

class FileInfo(BaseModel):
    id: str
    name: str
    size: int
    upload_date: datetime
    media_type: str

class Document(BaseModel):
    id: str
    files: List[FileInfo]
    document_type: Optional[str]
    note: Optional[str]

# DXSO Jobs models
class ProtocolEntry(BaseModel):
    text: str
    type: str
    filename: str
    time: datetime
    context: Optional[str] = None

class DXSOJob(BaseModel):
    ready: bool

# EXTF Files models
class ValidationDetails(BaseModel):
    error_code: str
    message: str

class ExtfJob(BaseModel):
    client_application_display_name: Optional[str]
    client_application_vendor: Optional[str]
    client_application_version: Optional[str]
    data_category_id: int
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    label: str
    number_of_accounting_records: int
    reference_id: Optional[str]
    result: str
    timestamp: datetime
    validation_details: Optional[ValidationDetails]

# Cash Register Models
class CashRegisterMetadata(BaseModel):
    document_type: str
    note: Optional[str]
    extensions: Dict[str, Any]

class Tenant(BaseModel):
    id: str
    name: Optional[str]

class TseLogInfo(BaseModel):
    serial_number: str
    max_signature_counter: Optional[int]
    custom_field: Optional[str]

# HR Documents Models
class HRClient(BaseModel):
    client_guid: str
    consultant_number: int
    client_number: int
    name: Optional[str]

class ClientsResponse(BaseModel):
    clients: List[HRClient]

# Master Data Models
class BrickContext(BaseModel):
    key: str
    bricks: Optional[List[str]]

class AppUpdate(BaseModel):
    brick_contexts: List[BrickContext]

class IdAndEtag(BaseModel):
    id: str
    etag: str

class SearchRequest(BaseModel):
    ids: Optional[List[str]]
    ids_and_updated: Optional[List[IdAndEtag]]

class MasterClientContainer(BaseModel):
    # Add relevant fields based on your needs
    pass

class MasterClientFull(BaseModel):
    id: str
    data_environment_number: int
    revision: Optional[str]
    etag: Optional[str]
    container: Optional[MasterClientContainer]

# HR eAU Models
class EauRequest(BaseModel):
    start_work_incapacity: str
    notification: Optional[Dict[str, Any]]
    contact_person: Optional[Dict[str, Any]]

class Feedback(BaseModel):
    feedback_id: str
    timestamp: str
    state: str
    automatic_feedback_until: Optional[str]

# HR Exports Models
class SocialSecurityPayments(BaseModel):
    employee_number: int
    payroll_accounting_month: str
    payroll_recalculation_month: Optional[str]
    social_security_contributions: Dict[str, float]

class TaxPayments(BaseModel):
    employee_number: int
    payroll_accounting_month: str
    payroll_recalculation_month: Optional[str]
    tax_payments: Dict[str, float]

class Absences(BaseModel):
    employee_number: int
    payroll_accounting_month: str
    total_vacation_entitlement: Optional[float]
    vacation_days_taken: Optional[float]
    remaining_vacation_days: Optional[float]
    sick_leave_month: Optional[float]
    overtime: Optional[float]

# HR Files Models
class JobInfo(BaseModel):
    job_id: str
    timestamp: str
    state: str

# HR Payroll Reports Models
class DocumentMetadataDto(BaseModel):
    employee_documents: List[Dict[str, Any]]
    client_documents: List[Dict[str, Any]]

class ClientWithAccessList(BaseModel):
    client_id: str
    consultant_number: int
    client_number: int
    document_types: Dict[str, List[str]] 