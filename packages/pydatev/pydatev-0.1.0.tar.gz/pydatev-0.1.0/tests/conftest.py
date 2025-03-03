"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from datetime import datetime
from typing import Generator, AsyncGenerator

from pydatev.app.main import app
from pydatev.app.models.base import Client, ClientWithServices, Service 

@pytest.fixture
def test_client() -> Generator:
    """Create a test client for FastAPI app."""
    with TestClient(app) as client:
        yield client

@pytest.fixture
async def async_client() -> AsyncGenerator:
    """Create an async test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_access_token() -> str:
    """Provide a mock access token."""
    return "mock_access_token"

@pytest.fixture
def mock_client_data() -> Client:
    """Provide mock client data."""
    return Client(
        client_number=12345,
        consultant_number=67890,
        id="test-client-id",
        name="Test Client"
    )

@pytest.fixture
def mock_client_with_services() -> ClientWithServices:
    """Provide mock client data with services."""
    return ClientWithServices(
        client_number=12345,
        consultant_number=67890,
        id="test-client-id",
        name="Test Client",
        services=[
            Service(
                name="accounting",
                scopes=["read", "write"]
            )
        ]
    )

@pytest.fixture
def mock_document_data() -> dict:
    """Provide mock document data."""
    return {
        "id": "doc-123",
        "files": [{
            "id": "file-123",
            "name": "test.pdf",
            "size": 1024,
            "upload_date": datetime.now().isoformat(),
            "media_type": "application/pdf"
        }],
        "document_type": "invoice",
        "note": "Test document"
    } 