"""Tests for frontend pages."""
import pytest
from unittest.mock import patch, MagicMock
import streamlit as st
from datev_api.frontend.app import (
    show_clients_page,
    show_documents_page,
    show_hr_services_page
)

def test_show_clients_page():
    """Test clients page display."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "client_number": 12345,
            "consultant_number": 67890,
            "id": "test-id",
            "name": "Test Client",
            "services": []
        }
    ]
    
    with patch('datev_api.frontend.app.authenticated_request', return_value=mock_response):
        with patch('streamlit.dataframe') as mock_dataframe:
            show_clients_page()
            mock_dataframe.assert_called_once()

def test_show_documents_page():
    """Test documents page display."""
    with patch('streamlit.file_uploader') as mock_uploader:
        with patch('streamlit.text_input') as mock_input:
            show_documents_page()
            mock_uploader.assert_called_once_with("Choose a file")
            mock_input.assert_called()

def test_show_hr_services_page():
    """Test HR services page display."""
    with patch('streamlit.tabs') as mock_tabs:
        show_hr_services_page()
        mock_tabs.assert_called_once_with(
            ["eAU Requests", "Employee Data", "Payroll Reports"]
        ) 