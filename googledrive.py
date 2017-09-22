#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 22:07:46 2017

@author: nicolaslelievre
"""


from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None



def create_credentials(scope):
    """
    -------------------------------------------------------------------------------------------------
    Description: Function that generates the credential file related to the scope provided
    and store it the .credentials folder of the home directory
    
    Input-value: String taking one of the following values:
        - https://www.googleapis.com/auth/drive
        - https://www.googleapis.com/auth/drive.readonly
        - https://www.googleapis.com/auth/drive.appfolder
        - https://www.googleapis.com/auth/drive.file
        - https://www.googleapis.com/auth/drive.install
        - https://www.googleapis.com/auth/drive.metadata
        - https://www.googleapis.com/auth/drive.metadata.readonly
        - https://www.googleapis.com/auth/drive.scripts    
    
    Output-value: N/A
    
    Example: create_credentials("https://www.googleapis.com/auth/drive.metadata")
    -------------------------------------------------------------------------------------------------
    """

    # Create a list of available scopes
    available_scopes = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/drive.appfolder',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive.install',
            'https://www.googleapis.com/auth/drive.metadata',
            'https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/drive.scripts'
            ]
    
    # Check if the scope exists
    if scope in available_scopes:
        
        # Get the path of your home directory
        home_dir = os.path.expanduser('~')
        
        # Get the path of the .credentials folder (in home directory)
        credential_dir = os.path.join(home_dir, '.credentials')
        
        # Create the .credentials folder if it does not exist
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        
        # Store the path of the google drive client secret file
        client_secret_path = os.path.join(credential_dir,'client_secret_google_drive_api.json')
        
        # Check if the client secret file exists
        if not os.path.exists(client_secret_path):
            result = """
            The client_secret_google_drive_api.json file does not exist.
            Credentials cannot be created without this file.
            Please follow these instructions to create the client secret file:
                1 - Use the following link to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.
                    Link: https://console.developers.google.com/start/api?id=drive
                2 - On the Add credentials to your project page, click the Cancel button.
                3 - At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.
                4 - Select the Credentials tab, click the Create credentials button and select OAuth client ID.
                5 - Select the application type Other, enter the name "Google Drive API Python", and click the Create button.
                6 - Click OK to dismiss the resulting dialog.
                7 - Click the file_download (Download JSON) button to the right of the client ID.
                8 - Move this file to the following location: """ + client_secret_path + """
                9 - Rename it to client_secret_google_drive_api.json
            """
        else:
            credential_name = "google_drive_api_scope_" + os.path.basename(scope).replace(".", "_") + ".json"
            credential_path = os.path.join(credential_dir,credential_name)
            
            store = Storage(credential_path)
            credentials = store.get()
            if not credentials or credentials.invalid:
                flow = client.flow_from_clientsecrets(client_secret_path, scope)
                flow.user_agent = 'Google Drive API Python'
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            result = 'The credentials have been created and stored here: ' + credential_path
    
    # If the scope does not exist send message
    else:
        result = """
              This scope provided does not exist.
              Here is the list of all available scopes:
                  - https://www.googleapis.com/auth/drive
                  - https://www.googleapis.com/auth/drive.readonly
                  - https://www.googleapis.com/auth/drive.appfolder
                  - https://www.googleapis.com/auth/drive.file
                  - https://www.googleapis.com/auth/drive.install
                  - https://www.googleapis.com/auth/drive.metadata
                  - https://www.googleapis.com/auth/drive.metadata.readonly
                  - https://www.googleapis.com/auth/drive.scripts
              """
    print(result)


def get_credentials(scope):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'google_drive_api_file.json')
    
    client_secret_path = os.path.join(credential_dir,
                                      'client_secret_google_drive_api.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_path, scope)
        flow.user_agent = 'Google Drive API Python'
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def credentials_exist(scope):
    """
    -------------------------------------------------------------------------------------------------
    Description: Check if the user have the credential of the scope provided
    
    Input-value: String taking one of the following values:
        - https://www.googleapis.com/auth/drive
        - https://www.googleapis.com/auth/drive.readonly
        - https://www.googleapis.com/auth/drive.appfolder
        - https://www.googleapis.com/auth/drive.file
        - https://www.googleapis.com/auth/drive.install
        - https://www.googleapis.com/auth/drive.metadata
        - https://www.googleapis.com/auth/drive.metadata.readonly
        - https://www.googleapis.com/auth/drive.scripts    
    
    Output-value: Boolean - True if credentials exist and False if not
    
    Example: create_exist("https://www.googleapis.com/auth/drive.metadata")
    -------------------------------------------------------------------------------------------------
    """
    result = False
     # Create a list of available scopes
    available_scopes = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/drive.appfolder',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive.install',
            'https://www.googleapis.com/auth/drive.metadata',
            'https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/drive.scripts'
            ]
    
    # Check if the scope exists
    if scope in available_scopes:
        
        # Get the path of your home directory
        home_dir = os.path.expanduser('~')
        
        # Get the path of the .credentials folder (in home directory)
        credential_dir = os.path.join(home_dir, '.credentials')
        
        # Store the path of the google drive client secret file
        client_secret_path = os.path.join(credential_dir,'client_secret_google_drive_api.json')
        
        # Check if the client secret file exists
        if not os.path.exists(client_secret_path):
            text = """
            The client_secret_google_drive_api.json file does not exist.
            Credentials cannot be created without this file.
            Please follow these instructions to create the client secret file:
                1 - Use the following link to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.
                    Link: https://console.developers.google.com/start/api?id=drive
                2 - On the Add credentials to your project page, click the Cancel button.
                3 - At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.
                4 - Select the Credentials tab, click the Create credentials button and select OAuth client ID.
                5 - Select the application type Other, enter the name "Google Drive API Python", and click the Create button.
                6 - Click OK to dismiss the resulting dialog.
                7 - Click the file_download (Download JSON) button to the right of the client ID.
                8 - Move this file to the following location: """ + client_secret_path + """
                9 - Rename it to client_secret_google_drive_api.json
            """
            print(text)
        else:
            credential_name = "google_drive_api_scope_" + os.path.basename(scope).replace(".", "_") + ".json"
            credential_path = os.path.join(credential_dir,credential_name)
            
            if os.path.exists(credential_path):
               result = True
            else:
                text = """
                The credentials for this scope do not exist.
                Use the create_credentials() function to generate the credentials
                """            
                print(text)
    # If the scope does not exist send message
    else:
        text = """
              The scope provided does not exist.
              Therefore the credentials cannot be checked.
              Here is the list of all available scopes:
                  - https://www.googleapis.com/auth/drive
                  - https://www.googleapis.com/auth/drive.readonly
                  - https://www.googleapis.com/auth/drive.appfolder
                  - https://www.googleapis.com/auth/drive.file
                  - https://www.googleapis.com/auth/drive.install
                  - https://www.googleapis.com/auth/drive.metadata
                  - https://www.googleapis.com/auth/drive.metadata.readonly
                  - https://www.googleapis.com/auth/drive.scripts
              """
        print(text)
    
    return(result)
    

def upload_file(file_path,folder_id):
    """
    -------------------------------------------------------------------------------------------------
    Description: Upload a local file in one google drive folder and print its ID once uploaded
    
    Input-values:
        - file_path: String containing the path of the file to be uploaded
        - folder_id: String containing the id of the folder
    
    Output-value: N/A
    
    Example: upload_file("/Users/TheDigitalHare/Images/picture1.jpg","0BwwA4oUTeiV1TGRPeTVjaWRDY1E")
    -------------------------------------------------------------------------------------------------
    """
    
    credentials = get_credentials("https://www.googleapis.com/auth/drive.file")
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    
    file_name = os.path.basename(file_path)
    
    file_metadata = {
            'name': file_name,
            'parents': [folder_id]}

    media = MediaFileUpload(file_path,resumable=True)
    
    file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
    
    print('The ID of the uploaded file is: %s' % file.get('id'))


