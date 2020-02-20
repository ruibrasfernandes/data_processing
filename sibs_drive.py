from apiclient.discovery import build
from apiclient import errors

from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http


from google.oauth2 import service_account
import googleapiclient.discovery
import io

from googleapiclient.http import MediaIoBaseDownload


def getSharedDriveFiles(service):

    results = service.drives().list().execute()
    items = results.get('drives', [])

    driveIDs = []

    if not items:
        print('No files found')
    else:
        print('Drives:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            driveIDs.append(item['id'])

    query = "name contains '.inp'"
    results = service.files().list(q=query, pageSize=2, fields='files(name, id)', driveId='0AG3pjV8_oFy2Uk9PVA',
                                   corpora='drive', includeItemsFromAllDrives=True, supportsAllDrives=True).execute()

    items = results.get('files', [])
    if not items:
        print('No files found')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


def downloadFile(drive, file_id, filename):
    request = drive.files().get_media(fileId=file_id)
    # fh = io.BytesIO()
    fh = io.FileIO(filename, 'wb') 
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))



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


userEmail = 'ruibras@lovignwalk.com'

http_auth = credentials.authorize(Http())

print('building drive')
try:
    drive = build('drive', 'v3', http=http_auth)
    print('success building drive')
except:
    print('failed building drive')

files = drive.files().list().execute().get('files', [])
for f in files:
    print(f['name'], f['mimeType'])

print('drive built or failed')

getSharedDriveFiles(drive)

fileId = '1O54W07mPZPYczdfJQeG7FXwupE0otY88'
downloadFile(drive, fileId, '201902070162.inp')