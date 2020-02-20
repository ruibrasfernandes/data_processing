import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('SA_sheet-write-access.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Helpo-SIBS').sheet1

test = sheet.get_all_records()
print(test)
