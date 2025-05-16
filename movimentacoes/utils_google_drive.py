import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
from django.conf import settings

# Caminho absoluto para o arquivo de credenciais
SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'config', 'drive_service_account.json')

# ID da pasta no Drive
DRIVE_FOLDER_ID = settings.GOOGLE_DRIVE_FOLDER_ID

def upload_file_to_drive(file, filename, replace_file_id=None):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=credentials)

    if replace_file_id:
        service.files().delete(fileId=replace_file_id)

    file_metadata = {
        'name': filename,
        'parents': [DRIVE_FOLDER_ID]
    }

    media = MediaIoBaseUpload(file, mimetype=file.content_type, resumable=True)
    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    return uploaded.get('webViewLink'), uploaded.get('id')
