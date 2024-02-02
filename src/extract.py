import pandas as pd
import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def extract_data_from_sheets(service, spreadsheet_id, range_name, date_column_name, start_date=None):
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    if not values:
        logging.info('No data found in the sheet.')
        return pd.DataFrame()
    else:
        df = pd.DataFrame(values[1:], columns=values[0])
        if start_date and date_column_name in df.columns:
            df[date_column_name] = pd.to_datetime(df[date_column_name])
            df = df[df[date_column_name] >= pd.to_datetime(start_date)]
        logging.info("Successfully extracted data from Google Sheets.")
        return df

def init_google_sheets_api(config):
    creds = Credentials.from_service_account_file(config['service_account_file'])
    service = build('sheets', 'v4', credentials=creds)
    logging.info("Successfully connected to Google Sheets Service.")
    return service
