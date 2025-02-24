import os
import sys
from src.DSProject.exception import CustomException
from src.DSProject.logger import logging
import pandas as pd
from src.DSProject.utils import read_sql_data
from sklearn.model_selection import train_test_split

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    # creating data paths
    train_data_path= os.path.join('artifacts', 'train.csv')
    test_data_path= os.path.join('artifacts', 'test.csv')
    raw_data_path= os.path.join('artifacts', 'raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config= DataIngestionConfig()


    def initiate_data_ingestion(self):
        try:
            #reading data from sql
            df= read_sql_data()
            logging.info("Reading completed from mysql database")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path))

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            train_set, test_set= train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            
            logging.info("Data ingestion completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)
        