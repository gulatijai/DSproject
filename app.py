from src.DSProject.logger import logging
from src.DSProject.exception import CustomException
from src.DSProject.components.data_ingestion import DataIngestion
from src.DSProject.components.data_ingestion import DataIngestionConfig
import sys

if __name__== "__main__":
    logging.info("The excecution has started")

    try:
        data_ingestion= DataIngestion()
        data_ingestion.initiate_data_ingestion()
       
    except Exception as e:
        logging.info("Custom exception")
        raise CustomException(e, sys)