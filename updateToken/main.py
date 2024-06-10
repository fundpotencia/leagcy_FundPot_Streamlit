import asyncio

from dotenv import load_dotenv
from datetime import datetime

from updateDB.create_service import create_services


def update_google_sheets(filename, folder_id, spreadsheet_id, token_sheet_name, token_str):
    """
    Updates a Google Sheets document and backs up existing files in Google Drive.

    This function performs the following steps:
    1. Backs up any existing file with the specified filename in the given folder.
    2. Updates the specified Google Sheets document by inserting the token string into cell A2 of the specified sheet.

    :param filename: Name of the file to search for and back up in Google Drive.
    :type filename: str.
    :param folder_id: ID of the Google Drive folder containing the file.
    :type folder_id: str.
    :param spreadsheet_id: ID of the Google Sheets document to update.
    :type spreadsheet_id: str.
    :param token_sheet_name: Name of the sheet in the Google Sheets document where the token will be inserted.
    :type token_sheet_name: str.
    :param token_str: Token string to be inserted into the Google Sheets document.
    :type token_str: str.
    """
    load_dotenv()
    services = asyncio.run(create_services())
    drive_service = services['drive']  # Get the Drive service
    sheets_service = services['sheets']  # Get the Sheets service


    # 1. Backup Existing File (if it exists)
    query = f"name = '{filename}' and '{folder_id}' in parents and trashed=false"
    existing_files = drive_service.files().list(q=query, fields='files(id, name)').execute().get('files', [])
    print("Existing files: ", existing_files)

    if existing_files:
        date_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        for file in existing_files:
            backup_name = f"backup_{date_suffix}_{file['name']}"
            copy_body = {'name': backup_name, 'parents': [folder_id]}
            drive_service.files().copy(fileId=file['id'], body=copy_body).execute()
            print(f'Backup created with name: {backup_name}')

    # 2. Update Google Sheets with the token string in cell A2
    token_range = f"{token_sheet_name}!A2"
    token_body = {
        'values': [[token_str]]
    }
    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=token_range,
        valueInputOption='RAW', body=token_body).execute()
    print(f"Token in Sheet {token_sheet_name} updated successfully.")
