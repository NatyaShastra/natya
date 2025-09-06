# Google Drive upload utility for annotated video and feedback summary
# Requires: google-api-python-client, google-auth-httplib2, google-auth-oauthlib
# Setup: See README for Google API credentials setup instructions

import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle


SCOPES = ['https://www.googleapis.com/auth/drive.file']
# Folder ID for your shared Google Drive folder
DRIVE_FOLDER_ID = '1iHwb0O5Rt311KWmGtm9pUaj2WtozN0zK'
# Always use the directory of this script for credentials and token
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(SCRIPT_DIR, 'token.pickle')
CREDENTIALS_PATH = os.path.join(SCRIPT_DIR, 'credentials.json')

def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file_to_drive(filepath, filename, mimetype):
    service = get_drive_service()
    file_metadata = {
        'name': filename,
        'parents': [DRIVE_FOLDER_ID]
    }
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded {filename} to Google Drive with file ID: {file.get('id')}")
    return file.get('id')

def upload_feedback_and_video(feedback_text, video_path, student_id):
    # Save feedback summary as a text file
    feedback_filename = f"{student_id}_feedback.txt"
    with open(feedback_filename, 'w') as f:
        f.write(feedback_text)
    # Upload feedback
    upload_file_to_drive(feedback_filename, feedback_filename, 'text/plain')
    # Upload video
    video_filename = os.path.basename(video_path)
    upload_file_to_drive(video_path, video_filename, 'video/mp4')
    # Optionally, remove local feedback file
    os.remove(feedback_filename)

# Example usage:
# upload_feedback_and_video('Your feedback summary here', '/path/to/video.mp4', 'student1')
