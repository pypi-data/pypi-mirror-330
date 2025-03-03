import streamlit as st
import requests
from datetime import datetime
import pandas as pd
from urllib.parse import urlencode
import secrets

# Configure the base URL for the FastAPI backend
BASE_URL = "http://localhost:8000"

# OAuth2 Configuration
AUTH_URL = "https://api.datev.de/auth/authorize"  # Update with actual DATEV auth URL
TOKEN_URL = "https://api.datev.de/auth/token"    # Update with actual DATEV token URL
CLIENT_ID = st.secrets["oauth"]["client_id"]      # Store in streamlit secrets
CLIENT_SECRET = st.secrets["oauth"]["client_secret"]
REDIRECT_URI = "http://localhost:8501/callback"   # Streamlit default port

def init_session_state():
    """Initialize session state variables"""
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "state" not in st.session_state:
        st.session_state.state = None

def login():
    """Handle OAuth2 login flow"""
    # Generate state parameter for CSRF protection
    state = secrets.token_urlsafe(32)
    st.session_state.state = state
    
    # Build authorization URL
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "scope": "openid profile email"  # Add required scopes
    }
    auth_url = f"{AUTH_URL}?{urlencode(params)}"
    
    st.markdown(f"""
        <a href="{auth_url}" target="_self">
            <button style="background-color:#4CAF50;color:white;padding:10px 24px;border:none;border-radius:4px;cursor:pointer;">
                Login with DATEV
            </button>
        </a>
    """, unsafe_allow_html=True)

def handle_callback():
    """Handle OAuth2 callback and token exchange"""
    query_params = st.experimental_get_query_params()
    
    if "code" in query_params and "state" in query_params:
        # Verify state parameter
        if query_params["state"][0] != st.session_state.state:
            st.error("Invalid state parameter")
            return
        
        # Exchange authorization code for access token
        try:
            response = requests.post(
                TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": query_params["code"][0],
                    "redirect_uri": REDIRECT_URI,
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                }
            )
            
            if response.status_code == 200:
                token_data = response.json()
                st.session_state.access_token = token_data["access_token"]
                # Clear query parameters
                st.experimental_set_query_params()
                st.success("Successfully logged in!")
                st.rerun()
            else:
                st.error("Failed to obtain access token")
        except Exception as e:
            st.error(f"Error during token exchange: {str(e)}")

def authenticated_request(method, url, **kwargs):
    """Make authenticated requests to the API"""
    if not st.session_state.access_token:
        st.error("Please log in first")
        return None
    
    headers = {
        "Authorization": f"Bearer {st.session_state.access_token}"
    }
    if "headers" in kwargs:
        headers.update(kwargs["headers"])
    kwargs["headers"] = headers
    
    response = requests.request(method, url, **kwargs)
    
    # Handle token expiration
    if response.status_code == 401:
        st.error("Session expired. Please log in again")
        st.session_state.access_token = None
        st.rerun()
    
    return response

def main():
    init_session_state()
    st.title("DATEV API Integration Dashboard")
    
    # Show login button if not authenticated
    if not st.session_state.access_token:
        login()
        handle_callback()
        return
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.access_token = None
        st.rerun()
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Select a Service",
        ["Clients", "Documents", "HR Services", "Cash Register", "Master Data"]
    )

    if page == "Clients":
        show_clients_page()
    elif page == "Documents":
        show_documents_page()
    elif page == "HR Services":
        show_hr_services_page()
    elif page == "Cash Register":
        show_cash_register_page()
    elif page == "Master Data":
        show_master_data_page()

def show_clients_page():
    st.header("Clients Management")
    
    # Client List
    st.subheader("Client List")
    try:
        response = authenticated_request("GET", f"{BASE_URL}/clients")
        if response and response.status_code == 200:
            clients = response.json()
            
            # Convert clients to DataFrame for better display
            clients_df = pd.DataFrame(clients)
            st.dataframe(clients_df)
            
            # Select specific client
            client_ids = [client['client_id'] for client in clients]
            selected_client = st.selectbox("Select a client for details", client_ids)
            
            if selected_client:
                client_response = authenticated_request("GET", f"{BASE_URL}/clients/{selected_client}")
                if client_response and client_response.status_code == 200:
                    st.json(client_response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching clients: {str(e)}")

def show_documents_page():
    st.header("Document Management")
    
    # Document Upload
    st.subheader("Upload Document")
    client_id = st.text_input("Client ID")
    uploaded_file = st.file_uploader("Choose a file")
    document_type = st.text_input("Document Type (optional)")
    note = st.text_area("Note (optional)")
    
    if uploaded_file and client_id and st.button("Upload"):
        try:
            files = {"file": uploaded_file}
            data = {
                "document_type": document_type,
                "note": note
            }
            response = authenticated_request(
                "POST",
                f"{BASE_URL}/clients/{client_id}/documents",
                files=files,
                data=data
            )
            if response and response.status_code == 201:
                st.success("Document uploaded successfully!")
                st.json(response.json())
            else:
                st.error(f"Upload failed: {response.text if response else 'No response'}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error uploading document: {str(e)}")

def show_hr_services_page():
    st.header("HR Services")
    
    tab1, tab2, tab3 = st.tabs(["eAU Requests", "Employee Data", "Payroll Reports"])
    
    with tab1:
        st.subheader("Create eAU Request")
        consultant_number = st.text_input("Consultant Number")
        client_number = st.text_input("Client Number")
        personnel_number = st.text_input("Personnel Number")
        
        # Add form fields for eAU request
        if st.button("Submit eAU Request"):
            if consultant_number and client_number and personnel_number:
                try:
                    # Add your eAU request logic here
                    st.info("eAU request submission would go here")
                except Exception as e:
                    st.error(f"Error submitting eAU request: {str(e)}")
    
    with tab2:
        st.subheader("Employee Data")
        # Add employee data viewing/management features
        
    with tab3:
        st.subheader("Payroll Reports")
        client_id = st.text_input("Client ID", key="payroll_client_id")
        period = st.text_input("Period (YYYY-MM)")
        
        if st.button("Get Payroll Documents"):
            if client_id and period:
                try:
                    response = authenticated_request(
                        "GET",
                        f"{BASE_URL}/payrollreports/clients/{client_id}/documents/{period}",
                        params={"document_types": ["ALL"]}
                    )
                    if response and response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to fetch payroll documents")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching payroll documents: {str(e)}")

def show_cash_register_page():
    st.header("Cash Register Management")
    
    st.subheader("Tenants")
    if st.button("Get Tenants"):
        try:
            response = authenticated_request(
                "GET",
                f"{BASE_URL}/tenants",
                headers={"Request-Id": str(datetime.now().timestamp())}
            )
            if response and response.status_code == 200:
                st.json(response.json())
            else:
                st.error("Failed to fetch tenants")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching tenants: {str(e)}")

def show_master_data_page():
    st.header("Master Data Management")
    
    st.subheader("Search Master Clients")
    search_term = st.text_input("Search Term")
    
    if st.button("Search") and search_term:
        try:
            search_request = {
                "searchTerm": search_term
            }
            response = authenticated_request(
                "POST",
                f"{BASE_URL}/master-clients/search",
                json=search_request
            )
            if response and response.status_code == 200:
                st.json(response.json())
            else:
                st.error("Search failed")
        except requests.exceptions.RequestException as e:
            st.error(f"Error searching master clients: {str(e)}")

if __name__ == "__main__":
    st.set_page_config(
        page_title="DATEV API Integration",
        page_icon="📊",
        layout="wide"
    )
    main() 