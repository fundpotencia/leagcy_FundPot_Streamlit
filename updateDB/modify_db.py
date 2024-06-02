from updateDB.create_service import create_services

# Define the credentials and the ID of the spreadsheet
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

async def replace_multiple_sheets(spreadsheet_id, sheet_data):
    """
    Replaces multiple Google Sheets sheets with DataFrames.

    This function clears the specified sheets, then fills them with data from corresponding DataFrames.
    DataFrames are converted to lists of lists for efficient uploading.

    :param spreadsheet_id: ID of the Google Sheets spreadsheet.
    :type spreadsheet_id: str
    :param sheet_data: A dictionary where keys are sheet names and values are DataFrames.
    :type sheet_data: dict
    """
    services, _ = await create_services()
    service = services['sheets']

    update_data = []  # List to hold update requests for batchUpdate

    for sheet_name, df in sheet_data.items():
        df = df.fillna("")  # Fill NaN values with empty strings
        num_columns = len(df.columns)
        column_letter = chr(ord('A') + num_columns - 1)
        range_all = f"{sheet_name}!A1:{column_letter}"

        # Clear the sheet
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id, range=range_all
        ).execute()

        # Convert DataFrame to a list of lists for upload
        values = [df.columns.values.tolist()] + df.reset_index(drop=True).values.tolist()

        # Create an update request for this sheet
        update_data.append({
            "range": f"{sheet_name}!A1",
            "values": values
        })

    # Perform a batch update to update all sheets at once
    body = {
        "valueInputOption": "RAW",
        "data": update_data
    }
    update = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id, body=body
    ).execute()

    print(f"Sheets updated successfully.")
