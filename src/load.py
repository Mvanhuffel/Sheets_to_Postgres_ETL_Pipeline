import logging
from sqlalchemy import create_engine

def insert_data_to_db(dataframe, engine, schema, table_name):
    dataframe.columns = [col.lower() for col in dataframe.columns]
    with engine.connect() as connection:
        dataframe.to_sql(table_name, connection, schema=schema, if_exists='append', index=False)
    logging.info(f"Data successfully loaded into {schema}.{table_name} table.")

def init_db_engine(config):
    engine = create_engine(f"postgresql://{config['db_username']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}")
    logging.info("Successfully connected to the database.")
    return engine
