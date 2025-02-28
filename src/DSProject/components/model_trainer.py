import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingRegressor,
    RandomForestRegressor
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor

from src.DSProject.exception import CustomException
from src.DSProject.logger import logging
from src.DSProject.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path= os.path.join("artifacts", 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.__model_trainer_config= ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )

            models= {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Booking": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            

            params= {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    #'spliter': ['best', 'randon'],
                    #'max_features': ['sqrt', 'log2']
                },
                 "Random Forest": {
                    #'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    #'spliter': ['best', 'randon'],
                    #'max_features': ['sqrt', 'log2']
                    'n_estimators': [8,16,32,64,128,256]
                 },
                 "Gradient Booking": {
                    #'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'learning_rate': [.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    #'spliter': ['best', 'randon'],
                    #'max_features': ['sqrt', 'log2']
                    'n_estimators': [8,16,32,64,128,256]
                 },
                 
                 'Linear Regression': {},

                 "XGBRegressor": {
                    #'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'learning_rate': [.1,.01,.05,.001],
                    #'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    #'spliter': ['best', 'randon'],
                    #'max_features': ['sqrt', 'log2']
                    'n_estimators': [8,16,32,64,128,256]
                 },
                 'CatBoosting Regressor':{
                     'depth': [6,8,10],
                     'learning_rate': [.1,.01,.05,.001],
                     'iterations': [30,50,100]
                 },
                 "AdaBoost Regressor": {
                    #'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'learning_rate': [.1,.01,.05,.001],
                    #'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    #'spliter': ['best', 'randon'],
                    #'max_features': ['sqrt', 'log2']
                    'n_estimators': [8,16,32,64,128,256]
                 }

            }
            model_report: dict= evaluate_models(X_train, y_train, X_test, y_test, models, params)

            ##To get the best model score
            best_model_score= max(sorted(model_report.values()))

            ## to get the best model name
            best_model_name= list(model_report.keys())[
                list(model_report.values()).index(best_model_score)]
            
            best_model= models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f" Best found model on boh training and testing dataset ")

            save_object(
                file_path= self.__model_trainer_config.trained_model_file_path,
                obj= best_model
            )

            predicted= best_model.predict(X_test)

            r2_square= r2_score(y_test, predicted)
            return r2_square

        except Exception as e:
            raise CustomException(e, sys)