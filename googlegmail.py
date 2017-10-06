#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 17:39:48 2017

@author: The Digital Hare
"""

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import base64
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
import httplib2

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None





def create_credentials(scope):
    """
    -------------------------------------------------------------------------------------------------
    Generate the credential file related to the scope provided
    and store it the .credentials folder of the home directory
    
    Input-value: String taking one of the following values:
        - https://www.googleapis.com/auth/gmail.readonly
        - https://www.googleapis.com/auth/gmail.compose
        - https://www.googleapis.com/auth/gmail.send
        - https://www.googleapis.com/auth/gmail.insert	
        - https://www.googleapis.com/auth/gmail.labels	
        - https://www.googleapis.com/auth/gmail.modify	
        - https://www.googleapis.com/auth/gmail.metadata
        - https://www.googleapis.com/auth/gmail.settings.basic
        - https://www.googleapis.com/auth/gmail.settings.sharing  
    
    Output-value: N/A
    
    Example: create_credentials("https://www.googleapis.com/auth/gmail.readonly")
    -------------------------------------------------------------------------------------------------
    """

    # Create a list of available scopes
    available_scopes = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.compose',
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/gmail.insert',
            'https://www.googleapis.com/auth/gmail.labels',
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.metadata',
            'https://www.googleapis.com/auth/gmail.settings.basic',
            'https://www.googleapis.com/auth/gmail.settings.sharing'  
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
        
        # Store the path of the google gmail client secret file
        client_secret_path = os.path.join(credential_dir,'client_secret_google_gmail_api.json')
        
        # Check if the client secret file exists
        if not os.path.exists(client_secret_path):
            result = """
            The client_secret_google_gmail_api.json file does not exist.
            Credentials cannot be created without this file.
            Please follow these instructions to create the client secret file:
                1 - Use the following link to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.
                    Link: https://console.developers.google.com/start/api?id=gmail
                2 - On the Add credentials to your project page, click the Cancel button.
                3 - At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.
                4 - Select the Credentials tab, click the Create credentials button and select OAuth client ID.
                5 - Select the application type Other, enter the name "Google Gmail API Python", and click the Create button.
                6 - Click OK to dismiss the resulting dialog.
                7 - Click the file_download (Download JSON) button to the right of the client ID.
                8 - Move this file to the following location: """ + client_secret_path + """
                9 - Rename it to client_secret_google_gmail_api.json
            """
        else:
            credential_name = "google_gmail_api_scope_" + os.path.basename(scope).replace(".", "_") + ".json"
            credential_path = os.path.join(credential_dir,credential_name)
            
            store = Storage(credential_path)
            credentials = store.get()
            if not credentials or credentials.invalid:
                flow = client.flow_from_clientsecrets(client_secret_path, scope)
                flow.user_agent = 'Google Gmail API Python'
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
                   - https://www.googleapis.com/auth/gmail.readonly
                   - https://www.googleapis.com/auth/gmail.compose
                   - https://www.googleapis.com/auth/gmail.send
                   - https://www.googleapis.com/auth/gmail.insert	
                   - https://www.googleapis.com/auth/gmail.labels	
                   - https://www.googleapis.com/auth/gmail.modify	
                   - https://www.googleapis.com/auth/gmail.metadata
                   - https://www.googleapis.com/auth/gmail.settings.basic
                   - https://www.googleapis.com/auth/gmail.settings.sharing  
              """
    print(result)

def get_credentials(scope):
    """
    Return the google drive credentials of the scope

    """
    
    if credentials_exist(scope):
        
        # Get the path of your home directory
        home_dir = os.path.expanduser('~')
            
        # Get the path of the .credentials folder (in home directory)
        credential_dir = os.path.join(home_dir, '.credentials')
        
        credential_name = "google_gmail_api_scope_" + os.path.basename(scope).replace(".", "_") + ".json"
        credential_path = os.path.join(credential_dir,credential_name)
    
        store = Storage(credential_path)
        credentials = store.get()
    
    return credentials


def credentials_exist(scope):
    """
    -------------------------------------------------------------------------------------------------
    Check if the user have the credential of the scope provided
    
    Input-value: String taking one of the following values:
        - https://www.googleapis.com/auth/gmail.readonly
        - https://www.googleapis.com/auth/gmail.compose
        - https://www.googleapis.com/auth/gmail.send
        - https://www.googleapis.com/auth/gmail.insert	
        - https://www.googleapis.com/auth/gmail.labels	
        - https://www.googleapis.com/auth/gmail.modify	
        - https://www.googleapis.com/auth/gmail.metadata
        - https://www.googleapis.com/auth/gmail.settings.basic
        - https://www.googleapis.com/auth/gmail.settings.sharing   
    
    Output-value: Boolean - True if credentials exist and False if not
    
    Example: create_exist("https://www.googleapis.com/auth/drive.metadata")
    -------------------------------------------------------------------------------------------------
    """
    result = False
     # Create a list of available scopes
    available_scopes = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.compose',
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/gmail.insert',
            'https://www.googleapis.com/auth/gmail.labels',
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.metadata',
            'https://www.googleapis.com/auth/gmail.settings.basic',
            'https://www.googleapis.com/auth/gmail.settings.sharing'
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
            The client_secret_google_gmail_api.json file does not exist.
            Credentials cannot be created without this file.
            Please follow these instructions to create the client secret file:
                1 - Use the following link to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.
                    Link: https://console.developers.google.com/start/api?id=gmail
                2 - On the Add credentials to your project page, click the Cancel button.
                3 - At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.
                4 - Select the Credentials tab, click the Create credentials button and select OAuth client ID.
                5 - Select the application type Other, enter the name "Google Gmail API Python", and click the Create button.
                6 - Click OK to dismiss the resulting dialog.
                7 - Click the file_download (Download JSON) button to the right of the client ID.
                8 - Move this file to the following location: """ + client_secret_path + """
                9 - Rename it to client_secret_google_gmail_api.json
            """
            print(text)
        else:
            credential_name = "google_gmail_api_scope_" + os.path.basename(scope).replace(".", "_") + ".json"
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
                  - https://www.googleapis.com/auth/gmail.readonly
                  - https://www.googleapis.com/auth/gmail.compose
                  - https://www.googleapis.com/auth/gmail.send
                  - https://www.googleapis.com/auth/gmail.insert	
                  - https://www.googleapis.com/auth/gmail.labels	
                  - https://www.googleapis.com/auth/gmail.modify	
                  - https://www.googleapis.com/auth/gmail.metadata
                  - https://www.googleapis.com/auth/gmail.settings.basic
                  - https://www.googleapis.com/auth/gmail.settings.sharing
              """
        print(text)
    
    return result



def SendMessage(sender, to, subject, message_text, file_paths=None):
    """
    Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.

    Returns:
    An object containing a base64url encoded email object.
    """
  
    credentials = get_credentials('https://www.googleapis.com/auth/gmail.send')
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
  
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    
    body = MIMEText(message_text)
    message.attach(body)
    
    if file_paths != None:
        
        for file_path in file_paths:
        
            content_type, encoding = mimetypes.guess_type(file_path)
            
            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)
            
            if main_type == 'text':
                fp = open(file_path, 'rb')
                msg = MIMEText(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(file_path, 'rb')
                msg = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(file_path, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(file_path, 'rb')
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())
                fp.close()
            
            encoders.encode_base64(msg)
            
            msg.add_header('Content-Disposition', 'attachment; filename=' + os.path.basename(file_path))
            message.attach(msg)
    
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    
    final_message = {'raw': raw}
    
    email = service.users().messages().send(userId='me', body=final_message).execute()
    
    return email['id']