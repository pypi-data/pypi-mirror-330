"""Tests for HR service endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

def test_get_hr_clients(test_client: TestClient):
    """Test getting HR clients."""
    mock_response = {
        "clients": [
            {
                "client_guid": "test-guid",
                "consultant_number": 12345,
                "client_number": 67890,
                "name": "Test HR Client"
            }
        ]
    }
    
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        response = test_client.get("/hr/clients")
        assert response.status_code == 200
        assert len(response.json()["clients"]) == 1

def test_create_eau_request(test_client: TestClient):
    """Test creating eAU request."""
    mock_response = {"location": "/eau-requests/123"}
    eau_request_data = {
        "start_work_incapacity": "2023-01-01",
        "notification": {"type": "test"},
        "contact_person": {"name": "Test Person"}
    }
    
    with patch('httpx.AsyncClient.post') as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.headers = {"Location": "/eau-requests/123"}
        
        response = test_client.post(
            "/clients/12345-67890/employees/123/eau-requests",
            json=eau_request_data
        )
        assert response.status_code == 201
        assert "location" in response.json() 