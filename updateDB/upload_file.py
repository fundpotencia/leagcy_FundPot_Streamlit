from datetime import datetime

from updateDB.create_service import create_services


async def upload_backup_file(filename, folder_id):
    """
    Uploads a backup of a file in a Google Drive folder.

    This function first checks if there are existing files with the same name in the folder.
    If there are, it creates a backup of each file with a prefix "backup" and the current date and time.

    :param file_path: Path of the file to backup.
    :type file_path: str.
    :param folder_id: ID of the Google Drive folder where the backup will be uploaded.
    :type folder_id: str.
    """
    services, _ = await create_services()
    drive_service = services['drive']

    # Searches for existing files with
    query = f"name = '{filename}' and '{folder_id}' in parents and trashed=false"
    existing_files = drive_service.files().list(q=query, fields='files(id, name)').execute().get('files', [])
    print("Existing files: ", existing_files)

    # If files exist, loads a copy with the prefix "backup" and the date
    if existing_files:
        date_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        for file in existing_files:
            backup_name = f"backup_{date_suffix}_{file['name']}"
            copy_body = {'name': backup_name, 'parents': [folder_id]}
            drive_service.files().copy(fileId=file['id'], body=copy_body).execute()
            print(f'Backup created with name: {backup_name}')