from django.shortcuts import render
from django.http import HttpResponse
import pickle
from googleapiclient.discovery import build
from  google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from file_extractor import views as fileExtractorView
import os
# Create your views here.
def register(request):
    verifyRegister()
    return HttpResponse('You have successfully registered')

def login(request):
    if verifyLogin():
        return render(request, 'authentication/login.html')

def verifyRegister():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        return HttpResponse('You have already registered')
    # If there are no (valid) credentials available, let the user log in.
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        fileExtractorView.init(creds)
        return True
    

def verifyLogin():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
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
            return HttpResponse('You have not registered')
    fileExtractorView.extractGoogleDoc(creds)
    return True
    

