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

    st.markdown(f"""
<div style='text-align: center;'>
    <h1 style='font-size: 30px;'><br>A autenticação falhou :(<br><br></h1>
    <h4>Por favor, faça login no link a seguir: <a target="_blank" href="{auth_url}">Autenticar</a></h4>
    <h3 style='font-size: 30px; color: white;'><br>Em caso de já ter realizado a autenticação, por favor recarregue a página! 
    Isso pode ser feito clicando no F5 ou no símbolo ⟳ do navegador</h3>
</div>
""", unsafe_allow_html=True)





