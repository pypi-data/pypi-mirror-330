from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATEV_CLIENT_ID: str
    DATEV_CLIENT_SECRET: str
    DATEV_REDIRECT_URI: str
    
    # API Base URLs
    ACCOUNTING_DOCS_API: str = "https://accounting-documents.api.datev.de/platform/v2"
    ACCOUNTING_DXSO_API: str = "https://accounting-dxso-jobs.api.datev.de/platform/v2"
    ACCOUNTING_EXTF_API: str = "https://accounting-extf-files.api.datev.de/platform/v3"
    ACCOUNTING_CLIENTS_API: str = "https://accounting-clients.api.datev.de/platform/v2"
    
    # Auth URLs
    AUTH_URL: str = "https://login.datev.de/openid/authorize"
    TOKEN_URL: str = "https://api.datev.de/token"
    
    # Additional API Base URLs
    CASH_REGISTER_API: str = "https://cashregister.api.datev.de/platform/v2"
    HR_DOCUMENTS_API: str = "https://hr-documents.api.datev.de/platform/v1"
    MASTER_DATA_API: str = "https://master-data-master-clients.api.datev.de/platform/v3"
    MYTAX_HEALTH_API: str = "https://mytax-income-tax-documents.api.datev.de/platform"
    
    # HR API Base URLs 
    HR_EAU_API: str = "https://eau.api.datev.de/platform/v1"
    HR_EXPORTS_API: str = "https://hr-exports.api.datev.de/platform/v1"
    HR_FILES_API: str = "https://hr-files.api.datev.de/platform/v1" 
    HR_PAYROLLREPORTS_API: str = "https://hr-payrollreports.api.datev.de/platform/v1"
    
    class Config:
        env_file = ".env"

settings = Settings() 