# Google Drive API


## Step 1: Turn on the Drive API

1. Use [this wizard](https://console.developers.google.com/start/api?id=drive) to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.
2. On the Add credentials to your project page, click the Cancel button.
3. At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.
4. Select the Credentials tab, click the Create credentials button and select OAuth client ID.
5. Select the application type Other, enter the name "Drive API Quickstart", and click the Create button.
6. Click OK to dismiss the resulting dialog.
7. Click the file_download (Download JSON) button to the right of the client ID.
8. Rename it `client_secret_google_drive_api.json` and keep it for the next step

## Step 2: Create a hidden folder to store your credentials

Run the following command that will create a hidden folder `.credentials` in your home directory.

```
mkdir ~/.credentials
```
Move the `client_secret_google_drive_api.json` file in the .credentials folder. 

Note that you can show the hidden files in your folder using the following shorcut:`Shift + Command + .`.

## Step 3: Install the Google Client Library

Run the following command to install the library using pip:

```
pip install --upgrade google-api-python-client
```

## Step 4: Generate the credentials files

