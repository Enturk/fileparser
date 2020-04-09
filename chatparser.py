#!/usr/bin/python

# main variables
input_dir = "PastChats"
fileSuffix = '.txt' # filetype we're looking for
startMarker = "From  " # marks beginning of substring after which the snippet is extracted
stopMarker = " : " # marks end of snippet to extract
output_dir = "TestOutput"
# testing done on a small number of known files
numberOfFiles = 4 # set to 0 if not testing
logfile = "chatparser.log"

if __name__ == "__main__":
    Verbose = True
else:
    Verbose = False

import time
ts = time.gmtime()
timestamp = time.strftime('%Y-%m-%d+%H-%M-%S', ts)

import logging
if Verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(filename=logfile, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.info(f'New script run on: {timestamp}')

# parse command line options
import getopt
import sys
try:
    options, remainder = getopt.getopt(
        sys.argv[1:],
        'i:o:t:v',
        ['input=',
         'output=',
         'testing=',
         'verbose',
         ])
except getopt.GetoptError as err:
    logging.error(f'ERROR: {err}')
    logging.error('The only options this script can process are:')
    logging.error(f'-i or --input [input directory]: use [input directory] instead of {input_dir}')
    logging.error(f'-o or --output [output directory]: use [output directory] instead of {output_dir}')
    logging.error('-t or --testing [integer]: run in test mode, only process first [integer] files in input directory')
    logging.error('-v or --verbose: very verbose feedback on script activity')
    sys.exit(1)

for opt, arg in options:
    if opt in ('-i', '--input'):
        input_dir = arg
    elif opt in ('-o', '--output'):
        output_dir = arg
    elif opt in ('-t', '--testing'):
        numberOfFiles = int(arg)
    elif opt in ('-v', '--verbose'):
        Verbose = True
       
if Verbose:
    logging.info('ARGV            : {sys.argv[1:]}')
    logging.info('Input Directory : {input_dir}')
    logging.info('Output Directory: {output_dir}')
    logging.info('Number of files : {numberOfFiles}')
    logging.info('Verbose         : {Verbose}')
    logging.info('REMAINING       : {remainder}')
    
# for folder navigation
import os
# script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
script_dir = os.getcwd()
if os.path.exists(os.path.join(script_dir, input_dir)):
    input_dir = os.path.join(script_dir, input_dir)
    logging.info(f'Current input directory is {input_dir}')
else:
    logging.critical(f'Fatal error - input directory {input_dir} not found')
    sys.exit(1)

if os.path.exists(os.path.join(script_dir, output_dir)):
    output_dir = os.path.join(script_dir, output_dir)
    logging.info(f'Current output directory is {input_dir}')
else:
    logging.critical(f'Fatal error - output directory {output_dir} not found')
    sys.exit(1)

# dict to track of number of contributions for each user
userDict = {}

# adds new user to dict, increments existing user count by one
def processUser(user):
    if user in userDict:
        userDict[user] = userDict[user] +1
        logging.debug(f'processChatLine: User {user} was added to dicitonary')
    else:
        userDict[user] = 1
        logging.debug(f'processChatLine: User {user} incremented in dictionary')

def parseLine(line, start, stop):
    if start not in line or stop not in line:
        logging.warning(f'parseLine failed to find substring {start} or {stop} in string:\n{line}')
        return -1
    else:
        begin = line.find(start) + len(start)
        end = line.find(stop)
        snippet = line[begin:end]
        logging.info(f'parseLine found {snippet} in this line:\n{line}')
        return snippet

#examine every file in folder
fileCount = 0
import os.path
for input_dir, dirnames, filenames in os.walk("."):
    for filename in [f for f in filenames if f.endswith(fileSuffix)]:

    #for filename in os.listdir(input_dir):
        if filename[-4:] != fileSuffix:
            logging.debug(f'Main: skipping {filename} because not a txt file.')
            continue
        logging.debug(f'Main: attempting to open {filename} in \n{input_dir}')
        with open(os.path.join(input_dir, filename), encoding = "ISO-8859-1") as f:
            logging.info(f'Main: opened {filename}')
            for line in f:
                user = parseLine(line, startMarker, stopMarker)
                if user != -1:
                    processUser(user)
        logging.debug(f'Finished with file {filename}. Here is what we got:')
        logging.debug(userDict)
        if numberOfFiles > 0:
            fileCount += 1
            if fileCount == numberOfFiles:
                logging.debug(f'Stopping because {fileCount} files procesed')
                break
