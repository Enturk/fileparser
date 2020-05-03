# fileparser

Takes a folder (and any subfolders) of text files and counts the occurrences of a substring defined by limiters in the files' lines.

## Requirements

An input folder, by default named *PastChats*, and an output folder, by default named *TestOutput*. Uses Python 3.7. OS neutral, in theory.

## Google API

To use the API with python, you need to enable it here: [https://developers.google.com/sheets/api/quickstart/python](https://developers.google.com/sheets/api/quickstart/python "Google API for Python")

And then, install the library (the above link has some troubleshooting steps):
```
$ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
