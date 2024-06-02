import streamlit as st
import warnings

from dotenv import load_dotenv
from updateDB.upload_file import upload_backup_file
from updateDB.modify_db import replace_multiple_sheets


warnings.filterwarnings("ignore", category=UserWarning, message=".*Arrow table.*")

async def run_updateDB(folderID, sheetID, filename, sheet_name, token_sheet_name):
    """
    Runs the database update process.

    This function uploads a backup file and replaces a Google Sheets sheet with a DataFrame.

    :param folderID: ID of the Google Drive folder where the backup file will be uploaded.
    :type folderID: str.
    :param sheetID: ID of the Google Sheets sheet that will be replaced.
    :type sheetID: str.
    :param filename: Name of the backup file.
    :type filename: str.
    :param sheet_name: Name of the sheet in the Google Sheets document.
    :type sheet_name: str.
    :param token_sheet_name: Name of the token sheet in the Google Sheets document.
    :type token_sheet_name: str.
    """

    load_dotenv()
    folder_id = folderID
    file_name = filename
    sheet_id = sheetID
    df = st.session_state.df
    
    token_sheet_name = token_sheet_name
    dftoken = st.session_state.dftoken
    
    workbook = {
        sheet_name: df,
        token_sheet_name: dftoken
    }

    await upload_backup_file(file_name, folder_id)
    await replace_multiple_sheets(sheet_id, workbook)