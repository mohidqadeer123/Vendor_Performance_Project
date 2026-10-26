import pandas as pd
import os
from sqlalchemy import create_engine
from google.colab import drive
import logging
import time

logging.basicConfig(filename = '/content/drive/MyDrive/logs/ingestion_db.log',
                    level = logging.DEBUG,
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    filemode = 'a')

engine = create_engine('sqlite:///inventory.db')

def ingest_db(df, table_name, connection):
  '''this function will ingest dataframe in db using an active connection'''
  df.to_sql(table_name, con = connection, if_exists = 'replace', index = False)

def load_raw_data():
  '''this function will load the csvs as dataframe and ingest in db safely using transactions'''
  start = time.time()
  
  # Using engine.begin() ensures safe transaction boundaries and automatic rollback on failure
  with engine.begin() as connection:
    for file in os.listdir(data_folder_path):
      if '.csv' in file:
        try:
          df = pd.read_csv(os.path.join(data_folder_path, file))
          logging.info(f'Ingesting {file} in db')
          ingest_db(df, file[:-4], connection)
        except Exception as e:
          logging.error(f'Failed to ingest {file}: {str(e)}')
          raise e
          
  end = time.time()
  total_time_taken = (end - start)/60
  logging.info(f'Ingestion Complete')
  logging.info(f'Total Time Taken: {total_time_taken}')

if __name__ == '__main__':
  load_raw_data()
