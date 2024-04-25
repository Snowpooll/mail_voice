# gmail_utils.py
import os.path
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
import email
import dateutil.parser

# スコープの設定
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def decode(encoded):
    decoded_bytes = base64.urlsafe_b64decode(encoded.encode('ASCII'))
    decoded_message = decoded_bytes.decode('utf-8')
    return decoded_message

def extract_urls(text):
    url_pattern = r'https?://\S+|www\.\S+'
    urls = re.findall(url_pattern, text)
    text_no_urls = re.sub(url_pattern, '', text)
    return urls, text_no_urls

def gmail_get_latest_unread_message_body(service, labelIdsValue):
    messages = service.users().messages()
    msg_list = messages.list(userId='me', labelIds=[labelIdsValue], q="is:unread", maxResults=1).execute()

    if 'messages' not in msg_list:
        return "No unread messages found.", []

    msg = msg_list['messages'][0]
    msg_id = msg['id']
    msg = messages.get(userId='me', id=msg_id, format='full').execute()

    date = gmail_get_messages_body_date(msg)

    body = ""
    if 'parts' in msg['payload']:
        for part in msg['payload']['parts']:
            if part['mimeType'] == 'text/plain' and part['body']['size'] > 0:
                body = decode(part['body']['data'])
                break
    else:
        body = decode(msg['payload']['body']['data'])

    urls, body_no_urls = extract_urls(body)
    return date + "<br>" + body_no_urls, urls

def gmail_get_messages_body_date(msg):
    headers = msg['payload']['headers']
    date_header = next(header['value'] for header in headers if header['name'].lower() == 'date')
    date = dateutil.parser.parse(date_header).strftime("%Y-%m-%d_%H-%M-%S")
    return date

def gmail_init():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

