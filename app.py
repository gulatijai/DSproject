from src.DSProject.logger import logging
from src.DSProject.exception import CustomException
from src.DSProject.components.data_ingestion import DataIngestion
from src.DSProject.components.data_ingestion import DataIngestionConfig
from src.DSProject.components.data_transformation import DataTransfomationConfig, DataTransformation

import sys

if __name__== "__main__":
    logging.info("The excecution has started")

    try:
        data_ingestion= DataIngestion()
        train_data_path, test_data_path= data_ingestion.initiate_data_ingestion()
        
        #Data_Transformation_config= DataTransfomationConfig()
        data_transformation= DataTransformation()
        data_transformation.initiate_data_transformation(train_data_path, test_data_path)
       
    except Exception as e:
        logging.info("Custom exception")
        raise CustomException(e, sys)