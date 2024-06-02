import streamlit as st
from google_auth_oauthlib.flow import Flow


async def write_authorization_url(flow):
    """
    Generates an authorization URL for the OAuth flow.

    :param flow: The OAuth2 flow instance.
    :type flow: google_auth_oauthlib.flow.Flow.
    :return: The authorization URL.
    :rtype: str.
    """
    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt='consent'
    )
    return authorization_url

async def write_access_token(flow, code):
    """
    Fetches an access token using the authorization code.

    :param flow: The OAuth2 flow instance.
    :type flow: google_auth_oauthlib.flow.Flow.
    :param code: The authorization code obtained from the authorization URL.
    :type code: str.
    :return: The credentials containing the access token.
    :rtype: google.oauth2.credentials.Credentials.
    """
    flow.fetch_token(code=code)
    return flow.credentials


async def oauth_flow(client_secrets_dict, SCOPES):
    """
    Performs the OAuth flow to obtain credentials.

    This function initiates the OAuth flow, generates an authorization URL, and displays it to the user.
    The user is expected to authorize the application and provide an authorization code.

    :param client_secrets_dict: The client secrets JSON dictionary.
    :type client_secrets_dict: dict.
    :param SCOPES: The list of scopes for which authorization is being requested.
    :type SCOPES: list.
    """

    redirect_uri = 'https://itajrredirect.streamlit.app/'

    if 'web' in client_secrets_dict:
        flow = Flow.from_client_config(
        client_secrets_dict,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    else:
        st.error("The client secrets JSON must contain the key 'web'.")            
        return

    auth_url = await write_authorization_url(flow=flow)
    st.markdown("<h1 style='text-align: center; font-size: 30px;'><br>A autenticação falhou :(</h1>", unsafe_allow_html=True)

    st.markdown(f'''<h4> Por favor, faça login no link a seguir: <a target="_self" href="{auth_url}"> Autenticar </a></h4>''',
             unsafe_allow_html=True)
