""" this script pulls data from the google spreadsheet. Then:
if a the first cell in the row of pulled data is the same as the one in the most recent csv file in subdir,
    it adds the new data at the end of that row (column L or M).
Otherwise, it adds it the csv data to the bottom,
and pushes it all back up.
"""

from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging

#important variables
Debug = True
subdir = "TestOutput"
if Debug:
    EarlyClass = True
    filename = "Output_2020-05-03+16-44-15"
    sheet = "API Test"
else:
    day = input('Are we doing a Monday or Tuesday class? (y/n)')
    if day[0] in ['y','Y']:
        EarlyClass = True
    else:
        EarlyClass = False
    filename = input('Please paste the filename here: ')
    sheet = input('Please type the EXACT name of the sheet you want to upload to')
csvfile = filename + ".csv"

# source:

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Wo8rJrC9yb-nqrRon81GDpmPaqIR4dYbUzDFKaBvH7U'
SAMPLE_RANGE_NAME = sheet + '!A:M'

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

#TODO move this stuff into main?

# check path
script_dir = os.getcwd()
if os.path.exists(os.path.join(script_dir, subdir)):
    input_path = os.path.join(script_dir, subdir)
    logging.info(f'Current input directory is {input_path}')
else:
    logging.critical(f'Fatal error - input directory {input_dir} not found')
    sys.exit(1)

# look for most recent file
##import glob
##list_of_csv_files = glob.glob(input_path + '*.csv')
##logging.info(f"Files in input folder:\n{list_of_csv_files}")
##csvfile = max(list_of_csv_files, key=os.path.getctime)
##files = sorted(os.listdir(input_path), key=os.path.getctime) # getcttime throws error
##i = len(files)
##while i >= 0:
##    i -= 1
##    if files[i][-4:] == ".csv":
##        csvfile = files[i]
##        break
##if i < 0:
##    logging.critical(f"No csv files in {input_path}")
##    sys.exit(1)

# get data from file
file = os.path.join(input_path, csvfile)
import csv
with open(file, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
logging.info(f"Imported data from {csvfile}:\n{data}")

# append the points at the right place
names = []
for row in data:
    if EarlyClass:
        names.append([row[0],None,None,None,None,None,None,None,None,None,None,20])
    else:
        names.append([row[0],None,None,None,None,None,None,None,None,None,None,None,20])

#merges two lists of lists based on first element, and major trumps minor
def list_merger(majorList, minorList):
    logging.debug("In list-merger. Here are the lists' first elements:")
    logging.warning(majorList[0])
    logging.warning(minorList[0])

    if not type(majorList[0]) == list or not type(minorList[0]) == list:
        logging.warning(f"One of the lists doesn't have sublists. Here is their first element:")
        return -1

    final_list = []    
    # check what's already in majorList
    for majorRow in majorList:
        if majorRow == None or majorRow == '' or majorRow == []:
            continue
        for minorRow in minorList:
            if minorRow == None or minorRow == '' or minorRow == []:
                minorRow.append("This row accounted for by Nazim's list_merger.")
                continue
            elif minorRow[-1] == "This row accounted for by Nazim's list_merger.":
                continue
            elif majorRow[0] == minorRow[0]:
                #found = True
                majorLen = len(majorRow)
                minorLen = len(minorRow)
                if majorLen > minorLen:
                    numelements = majorLen
                else:
                    numelements = minorLen
                i = 0
                while i < numelements:
                    if i >= majorLen: # no more major row
                        majorRow.append(minorRow[i])
                    elif (i < minorLen) and ((majorRow[i] == None) or (majorRow[i] == '')) and not ((minorRow[i] == None) or (minorRow[i] == '')):
                        # only adds minor row element if nothing in major row
                        majorRow[i] = minorRow[i]
                    else: # more major row than minor row
                        break
                    i += 1
                minorRow.append("This row accounted for by Nazim's list_merger.")
                break
        final_list.append(majorRow)

    # add in missing minorList rows
    for minorRow in minorList:
        if minorRow[-1] == "This row accounted for by Nazim's list_merger.":
            continue
        else:
            final_list.append(minorRow)
            
    return final_list

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

    service = build('sheets', 'v4', credentials=creds, cache_discovery=False) # True causes cache import error
    sheet = service.spreadsheets()

    # get the spreadsheet info
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        logging.info('No data found.')
    else:
        logging.debug(f'Values in {SAMPLE_RANGE_NAME}:')
        for row in values:
            logging.debug(row)

    # merge with values in csv file
    upload_data = list_merger(values, names)

    # upload the data
    values = upload_data
    body = {'values' : values}
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED", body=body
        ).execute()
    logging.info('{0} cells updated.'.format(result.get('updatedCells')))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
else:
    logging.basicConfig(level=logging.INFO, filename=logfile, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.info(f'New script run')
