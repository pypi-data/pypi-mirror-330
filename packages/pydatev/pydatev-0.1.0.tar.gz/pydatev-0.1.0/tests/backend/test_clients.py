"""Tests for client-related endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

def test_get_clients(test_client: TestClient, mock_client_with_services):
    """Test getting list of clients."""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [mock_client_with_services.dict()]
        
        response = test_client.get("/clients")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["client_number"] == mock_client_with_services.client_number

def test_get_client(test_client: TestClient, mock_client_with_services):
    """Test getting specific client details."""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_client_with_services.dict()
        
        response = test_client.get(f"/clients/{mock_client_with_services.id}")
        assert response.status_code == 200
        assert response.json()["id"] == mock_client_with_services.id

def test_get_client_not_found(test_client: TestClient):
    """Test getting non-existent client."""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Client not found"
        
        response = test_client.get("/clients/non-existent")
        assert response.status_code == 404 