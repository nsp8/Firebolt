# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:16:53 2019

@author: NishantParmar
"""
import os
import pandas as pd
import pickle
try:
    from apiclient import errors
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
except (ModuleNotFoundError, ImportError):
    os.system("pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    from apiclient import errors
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/spreadsheets.readonly']


def create_services():
    """Returns a service object.
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
                'gdrive_creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)
    sheets_service = build('sheets', 'v4', credentials=creds)
    
    return (drive_service, sheets_service)


def get_inputs_id(service, folder_id):
    query = "name contains 'inputs' and '{}' in parents".format(folder_id)
    try:
        response = service.files().list(q=query).execute()
        files = response.get('files', [])
        if len(files) == 0:
            return None
        if len(files) == 1:
            return files[0]['id']
        else:
            file_list = list()
            for file in files:
                file_list.append(file['id'])
            return file_list
    except errors.HttpError as error:
        print("ERROR in get_inputs_id: {}".format(error))


def get_folder_id(resultset, service_object):
    folders = resultset.get('files', [])
    if not folders:
        print("No files found.")
    else:
        print("Found target")
        if len(folders) == 1:
            print("\tFound folder: {}".format(folders[0]['name']))
            return folders[0]['id']
        else:
            print("Many folders")
            for folder in folders:
                print("\tTrying folder: {}".format(folder['name']))
                folder_id = folder['id']
                inputs_file_id = get_inputs_id(service_object, folder_id)
                if inputs_file_id:
                    return folder_id
            return None


def format_data(sheet_data):
    sheet_values = sheet_data["values"]
    if sheet_values:
        sheet_header, sheet_data = sheet_values[0], sheet_values[1:]
        sheet_df = pd.DataFrame(data=sheet_data, columns=sheet_header, 
                                index=None)
        
        return sheet_df
    return pd.DataFrame()


def read_data(service, spreadsheetId):
    input_sheet_cols = "A:B"
    spreadsheet_dataframes = dict()
    try:
        request = service.spreadsheets().get(spreadsheetId=spreadsheetId)
        response = request.execute()
        if response:
            sheets = response["sheets"]
            for sheet in sheets:
                sheet_title = sheet["properties"]["title"]
                sheet_data = service.spreadsheets().values().get(
                        spreadsheetId=spreadsheetId, 
                        range="{}!{}".format(sheet_title, input_sheet_cols)
                        ).execute()
                if sheet_data:
                    formatted_data = format_data(sheet_data)
                    print(formatted_data.shape)
                    spreadsheet_dataframes[sheet_title] = formatted_data
                
    except errors.HttpError as error:
        print("ERROR in handle_inputs: {}".format(error))
    finally:
        return spreadsheet_dataframes


def handle_inputs(user):
    file_data = None
    if user:
        drive_service, sheets_service = create_services()
        folder_condition = "mimeType = 'application/vnd.google-apps.folder'"
        folder_query = "name contains '{q}' and {t}".format(
                q=user, t=folder_condition)
        print(folder_query)
        try:
            response = drive_service.files().list(
                    q=folder_query,
                    fields="files(id, name)").execute()
            folder_id = get_folder_id(response, drive_service)
            if folder_id:
                inputs_file_id = get_inputs_id(drive_service, folder_id)
                print(inputs_file_id)
                file_data = read_data(sheets_service, inputs_file_id)
            else:
                print("No Folder found!")
        except errors.HttpError as error:
            print("ERROR in handle_inputs: {}".format(error))
            return None
    return file_data
