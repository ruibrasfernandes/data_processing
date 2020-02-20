from apiclient.discovery import build
import googleapiclient.discovery
from googleapiclient.http import MediaIoBaseDownload

from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account

from httplib2 import Http
import io

# https://developers.google.com/identity/protocols/googlescopes#drivev3
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/tasks'
]
SERVICE_ACCOUNT_FILE = './SA_sheet-write-access.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE, SCOPES)

# ...

http_auth = credentials.authorize(Http())

def get_sibs_files():

    service = build('drive', 'v3', http=http_auth)

    results = service.drives().list().execute()
    items = results.get('drives', [])

    driveIDs = []

    """ if not items:
        print('No files found')
    else:
        print('Drives:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            driveIDs.append(item['id']) """

    query = "name contains '.inp'"
    results = service.files().list(q=query, fields='files(name, id)', driveId='0AG3pjV8_oFy2Uk9PVA',
                                   corpora='drive', includeItemsFromAllDrives=True, supportsAllDrives=True).execute()

    items = results.get('files', [])
    
    return(items)



def read_file():
    
    service = build('drive', 'v3', http=http_auth)

    """ files = drive.files().list().execute().get('files', [])
    for f in files:
        print(f['name'], f['mimeType']) """
    
    file_id = '1O54W07mPZPYczdfJQeG7FXwupE0otY88'
    
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    # fh = io.FileIO(filename, 'wb') 
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    
    return(fh)










