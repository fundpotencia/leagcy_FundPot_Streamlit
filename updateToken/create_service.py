import streamlit as st
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from streamlit_local_storage import LocalStorage


localS = LocalStorage()


async def create_services():
    """
    Creates services for Google Drive and Google Sheets.

    This function first checks if there are valid credentials stored in the session state.
    If not, it initiates a login flow to get new credentials.
    The credentials are then used to create services for Google Drive and Google Sheets.

    :return: Dictionary containing the Google Drive and Google Sheets services.
    :rtype: dict.
    """
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

    # Load token from the JSON file

    # Checks if the token exists in the session_state and retrieves the credentials
    if 'token' in st.session_state:
        token_data = st.session_state['token']
        if isinstance(token_data, str):
            token_data = json.loads(token_data)
        creds = Credentials.from_authorized_user_info(token_data, SCOPES)

    # If there are no valid credentials, perform the login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        st.session_state['token'] = creds.to_json()

    # Creates services for Google Drive and Google Sheets
    services = {
        'drive': build('drive', 'v3', credentials=creds),
        'sheets': build('sheets', 'v4', credentials=creds)
    }

    return services
