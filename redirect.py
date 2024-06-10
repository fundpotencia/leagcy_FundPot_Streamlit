import streamlit as st
import urllib.parse
import json
import base64

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from updateToken.main import update_google_sheets


def transform_creds_dict(creds_dict):
    """
    Transforms a creds dictionary into the required token dictionary format.
    
    Args:
    creds_dict (dict): The dictionary to transform.

    Returns:
    dict: The transformed dictionary.
    """
    transformed_dict = {
        "token": creds_dict.get("token", ""),
        "refresh_token": creds_dict.get("_refresh_token", ""),
        "token_uri": creds_dict.get("_token_uri", "https://oauth2.googleapis.com/token"),
        "client_id": creds_dict.get("_client_id", ""),
        "client_secret": creds_dict.get("_client_secret", ""),
        "scopes": [
            "https://www.googleapis.com/auth/drive", 
            "https://www.googleapis.com/auth/spreadsheets"
        ],
        "universe_domain": creds_dict.get("_universe_domain", "googleapis.com"),
        "account": creds_dict.get("_account", ""),
        "expiry": creds_dict.get("expiry") if creds_dict.get("expiry") is not None else ""
    }
    
    return transformed_dict

def head():
        """
        Displays the header and the logo of the application
        """
        st.set_page_config(page_title="Autenticação", page_icon="✅")
        with open('./utils/front.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
        try:
            with open('./utils/logo_jr.png', 'rb') as logo_file:
                logo_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
                st.markdown(f'<p align="center"><img src="data:image/png;base64,{logo_base64}" width="500"></p>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("Logo file not found")
        st.markdown("<h1 style='text-align: center; font-size: 38px;'>Página de autenticação</h1>", unsafe_allow_html=True)

        st.markdown("<p style='text-align: center;'>>>> Página de autenticação <<<</p>", unsafe_allow_html=True)
        st.markdown(""" <div style="text-align: center; font-size: 20px;"> Aguarde enquanto a autenticação é feita. <br>Não é necessário realizar nenhuma operação! <br> <br></div>""", unsafe_allow_html=True)        

def Auth():
    # Load the client_secret_json from the secrets
    client_secret_json = st.secrets["general"]["client_secret_json"]
    client_config = json.loads(client_secret_json)

    # Instantiate the flow using the client_config
    flow = InstalledAppFlow.from_client_config(
        client_config,
        scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri='https://itajrredirect.streamlit.app/'
    )

    if "code" in st.query_params:
        st.info("Auntenticando... Esse processo pode demorar um pouco!")

        # Authentication was performed
        code = st.query_params["code"]
        decoded_code = urllib.parse.unquote(code)
        #st.write(f"Decoded code is: {decoded_code}")

        # Fetch the token and create credentials
        token = flow.fetch_token(code=decoded_code)
        creds = Credentials(token=token['access_token'],
                            refresh_token=token.get('refresh_token'),
                            token_uri=flow.client_config['token_uri'],
                            client_id=flow.client_config['client_id'],
                            client_secret=flow.client_config['client_secret'])

        # Transform and save token to session state
        if 'token' not in st.session_state:
            st.session_state['token'] = transform_creds_dict(creds.__dict__)
            #st.write("session state token", st.session_state['token'])

        aux_token_str = json.dumps(st.session_state['token'])

        # List of tables to update
        tables = ["dAlunos", "dPrem", "dEntrevistas"]

        for table in tables:
            filename = st.secrets[table]["filename"]
            folder_id = st.secrets[table]["folderID"]
            file_id = st.secrets[table]["fileID"]
            token_sheet_name = st.secrets[table]["token_sheet_name"]


            # Update the token in the token sheet
            update_google_sheets(
                filename = filename,
                folder_id = folder_id,
                token_str = aux_token_str,
                spreadsheet_id = file_id,
                token_sheet_name = token_sheet_name
            )
    else:
        link_url = "https://fundpot-itajr-home.streamlit.app/"
        st.markdown (f'''<h5> Usuário já autenticado! Clique aqui para voltar à página principal: <a target="_self" href="{link_url}">🏠 Home</a></h5>''', unsafe_allow_html=True)


head()
if Auth():
    st.success("Usuário autenticado com sucesso!")
    link_url = "https://fundpot-itajr-home.streamlit.app/"
    st.info (f'''text-align: center;<h5>Autenticação concluída! Clique aqui para voltar à página principal: <a target="_self" href="{link_url}">🏠 Home</a></h5>''', unsafe_allow_html=True)
