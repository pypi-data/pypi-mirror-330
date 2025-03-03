"""Tests for document-related endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

def test_get_document_types(test_client: TestClient):
    """Test getting document types."""
    mock_types = [
        {"name": "invoice", "category": "accounting", "debit_credit_identifier": "D"},
        {"name": "receipt", "category": "accounting", "debit_credit_identifier": "C"}
    ]
    
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_types
        
        response = test_client.get("/clients/test-client/document-types")
        assert response.status_code == 200
        assert len(response.json()) == 2

def test_upload_document(test_client: TestClient, mock_document_data):
    """Test document upload."""
    with patch('httpx.AsyncClient.post') as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = mock_document_data
        
        files = {"file": ("test.pdf", b"test content", "application/pdf")}
        data = {"document_type": "invoice", "note": "Test upload"}
        
        response = test_client.post(
            "/clients/test-client/documents",
            files=files,
            data=data
        )
        assert response.status_code == 201
        assert response.json()["id"] == mock_document_data["id"] 