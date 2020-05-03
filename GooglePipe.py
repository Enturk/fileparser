from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

EarlyClass = True

# source:
subdir = "TestOutput"
csvfile = 'Output_2020-05-03+16-44-15'
#TODO check tkinter for file selection GUI:
# https://docs.python.org/3/library/tk.html

# working off of https://developers.google.com/sheets/api/quickstart/python

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Wo8rJrC9yb-nqrRon81GDpmPaqIR4dYbUzDFKaBvH7U'
SAMPLE_RANGE_NAME = 'API Test!A:M'

# Change SCOPES below to generate authentication credentials.
# If modifying these scopes, delete the file token.pickle. See
# https://developers.google.com/sheets/quickstart/python#step_3_set_up_the_sample
#
# Authorize using one of the following scopes:
#     'https://www.googleapis.com/auth/drive'
#     'https://www.googleapis.com/auth/drive.file'
#     'https://www.googleapis.com/auth/drive.readonly'
#     'https://www.googleapis.com/auth/spreadsheets'
#     'https://www.googleapis.com/auth/spreadsheets.readonly'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


# get data from file
script_dir = os.getcwd()
if os.path.exists(os.path.join(script_dir, subdir)):
    input_path = os.path.join(script_dir, subdir)
    #logging.info(f'Current input directory is {input_path}')
else:
    #logging.critical(f'Fatal error - input directory {input_dir} not found')
    sys.exit(1)
file = os.path.join(input_path, csvfile + ".csv")
import csv
with open(file, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

names = [[]]
for row in data:
    if EarlyClass:
        names.append([row[0],None,None,None,None,None,None,None,None,None,None,20])
    else:
        names.append([row[0],None,None,None,None,None,None,None,None,None,None,None,20])
        
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # get the spreadsheet info
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('A, E:')
        for row in values:
            print(row)

    # upload the data
    values = names
    body = {'values' : values}
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED", body=body
        ).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


if __name__ == '__main__':
    main()
