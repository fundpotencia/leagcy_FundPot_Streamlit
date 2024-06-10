import streamlit as st
import pandas as pd
import json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from updateDB.oauth_flow import oauth_flow


async def create_services():
    """
    Creates services for Google Drive and Google Sheets.

    This function first checks if there are valid credentials stored in the session state or local storage.
    If not, it initiates a login flow to get new credentials.
    The credentials are then used to create services for Google Drive and Google Sheets.

    :return: Dictionary containing the Google Drive and Google Sheets services and the token string.
    :rtype: tuple(dict, str)
    """
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
    
    client_secret_json = st.secrets["general"]["client_secret_json"]
    client_secrets_dict = json.loads(client_secret_json)
    
    # Load token from the session state or file
    token_str = None
    if 'dftoken' in st.session_state:
        token_str = st.session_state.dftoken['Token'].astype(str).values[0]
        st.session_state['token'] = json.loads(token_str)

    if 'token' in st.session_state:
        creds = Credentials.from_authorized_user_info(st.session_state['token'], SCOPES)
        token_str = json.dumps(st.session_state['token'])
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            #st.info('Refreshing token')
            try:
                creds.refresh(Request())
                st.session_state['token'] = json.loads(creds.to_json())
                #st.success('Token refreshed')
            except Exception as e:
                #st.error(f"Token refresh failed: {e}")
                creds = None  # Force to go through the login flow
        if not creds or not creds.valid:
            creds = await oauth_flow(client_secrets_dict, SCOPES)
            print("oauth_flow returned:", creds)
        if creds:
            st.session_state['token'] = json.loads(creds.to_json())

    if creds and creds.valid:
        services = {
            'drive': build('drive', 'v3', credentials=creds),
            'sheets': build('sheets', 'v4', credentials=creds)
        }
        return services, token_str
    else:
        st.error("Failed to obtain valid credentials.")
        return None, None

