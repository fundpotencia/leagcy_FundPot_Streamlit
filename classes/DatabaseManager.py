import streamlit as st
import pandas as pd
import requests

from io import BytesIO
from urllib.parse import urlparse


class DatabaseManager:
    """
    Constructs a Database manager.
    """
    def __init__(self, sheetsID):
        """
        Initializes the DatabaseManager with the given Google Sheets ID.

        :param sheetsID: The ID of the Google Sheets document.
        :type sheetsID: str.
        """
        self.df = None
        self.url = f'https://docs.google.com/spreadsheets/d/{sheetsID}/export?format=xlsx'

    def is_valid_url(self, url):
        """
        Checks if a URL is valid.

        :param url: The URL to check.
        :type url: str.
        :return: True if the URL is valid, False otherwise.
        :rtype: bool.
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
    
    def save_db(self, df, token):
        """
        Saves the current dataframe and token to the database manager.

        :param df: Dataframe containing the data to be saved.
        :type df: pandas.DataFrame
        :param token: Token used for authentication.
        :type token: str
        """

        self.df = df
        self.dftoken = token

    def request_database(self, sheet_name, token_sheet_name):
        """
        Requests the database from the Google Sheets document.

        :return: The database as a DataFrame.
        :rtype: pandas.DataFrame.
        """
        if self.is_valid_url(self.url):
            response = requests.get(self.url)
            data = BytesIO(response.content)
            return pd.read_excel(data, sheet_name), pd.read_excel(data, token_sheet_name)
        else:
            st.error("A URL fornecida não é válida. Por favor, insira uma URL válida.")