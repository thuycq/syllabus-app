from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Đường dẫn file JSON service account
SERVICE_ACCOUNT_FILE = 'syllabus-app-drive-api.json'

# ID của folder Drive đích
FOLDER_ID = '1vtziPO7_zj7-JJlnxOqP568NV_nP1sK7'

# Tạo service kết nối Drive API
def create_drive_service():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

# Upload file lên Drive
def upload_file_to_drive(filename, filepath, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
    service = create_drive_service()

    file_metadata = {
        'name': filename,
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(filepath, mimetype=mimetype)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()

    print(f"Uploaded file: {file.get('name')} (ID: {file.get('id')})")
    print(f"View link: {file.get('webViewLink')}")
    return file.get('webViewLink')
