import sys
import logging
import yaml
from extract import extract_data_from_sheets, init_google_sheets_api
from load import insert_data_to_db, init_db_engine

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    logging.info("Configuration file loaded successfully.")
    return config

if __name__ == "__main__":
    print("ETL script started running.")
    config = load_config('config.yaml')

    logging.basicConfig(filename=config['log_file_path'], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        service = init_google_sheets_api(config)
        spreadsheet_id = config['file_id']
        range_name = 'Sheet1'
        date_column_name = config.get('date_column_name', 'default_date_column_name')
        start_date = sys.argv[1] if len(sys.argv) > 1 else None

        data = extract_data_from_sheets(service, spreadsheet_id, range_name, date_column_name, start_date)

        if not data.empty:
            engine = init_db_engine(config)
            insert_data_to_db(data, engine, config['schema_name'], config['staging_table_name'])
        else:
            logging.info("No data to load.")

    except Exception as e:
        logging.error(f"Error in ETL process: {e}")

    finally:
        logging.info("ETL process completed.")
