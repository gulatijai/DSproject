from src.DSProject.logger import logging
from src.DSProject.exception import CustomException
from src.DSProject.components.data_ingestion import DataIngestion
from src.DSProject.components.data_ingestion import DataIngestionConfig
from src.DSProject.components.data_transformation import DataTransfomationConfig, DataTransformation
from src.DSProject.components.model_trainer import ModelTrainerConfig, ModelTrainer

import sys

if __name__== "__main__":
    logging.info("The excecution has started")

    try:
        data_ingestion= DataIngestion()
        train_data_path, test_data_path= data_ingestion.initiate_data_ingestion()
        
        #Data_Transformation_config= DataTransfomationConfig()
        data_transformation= DataTransformation()
        train_arr, test_arr= data_transformation.initiate_data_transformation(train_data_path, test_data_path)

        #Model training
        model_trainer= ModelTrainer()
        print(model_trainer.initiate_model_trainer(train_arr, test_arr))
       
    except Exception as e:
        logging.info("Custom exception")
        raise CustomException(e, sys)