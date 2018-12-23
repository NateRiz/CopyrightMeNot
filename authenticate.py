import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from settings import *

class User:
    def __init__(self):
        self.user = None

    def authenticate(self):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        self.user = self.get_authenticated_service()

    def get_authenticated_service(self):
        CLIENT_SECRETS_FILE = os.path.join(os.getcwd(),"client_secret.json")
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
