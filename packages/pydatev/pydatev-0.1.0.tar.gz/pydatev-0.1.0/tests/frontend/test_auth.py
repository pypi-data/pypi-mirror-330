"""Tests for frontend authentication."""
import pytest
from unittest.mock import patch, MagicMock
import streamlit as st
from datev_api.frontend.app import login, handle_callback, init_session_state

def test_init_session_state():
    """Test session state initialization."""
    with patch('streamlit.session_state', {}):
        init_session_state()
        assert 'access_token' in st.session_state
        assert 'state' in st.session_state
        assert st.session_state.access_token is None

def test_login():
    """Test login function."""
    with patch('streamlit.markdown') as mock_markdown:
        with patch('secrets.token_urlsafe') as mock_token:
            mock_token.return_value = "test_state"
            login()
            mock_markdown.assert_called_once()
            assert "Login with DATEV" in mock_markdown.call_args[0][0]

def test_handle_callback_success():
    """Test successful callback handling."""
    mock_params = {
        "code": ["test_code"],
        "state": ["test_state"]
    }
    
    with patch('streamlit.experimental_get_query_params', return_value=mock_params):
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "access_token": "test_token"
            }
            
            with patch('streamlit.success') as mock_success:
                st.session_state.state = "test_state"
                handle_callback()
                mock_success.assert_called_once_with("Successfully logged in!") 