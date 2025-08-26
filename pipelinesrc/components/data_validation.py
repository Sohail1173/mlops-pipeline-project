import os
import sys
from pandas import DataFrame
import pandas as pd
from sklearn.model_selection import train_test_split
from pipelinesrc.entity.artifact_entity  import DataIngestionArtifact,DataValidationArtifact
from pipelinesrc.entity.config_entity  import DataIngestionConfig,DataValidationConfig
from pipelinesrc.exception import MyException
from pipelinesrc.logger import logging
from pipelinesrc.data_access.data_mongo import Proj1Data
from pipelinesrc.utils.main_utils import read_yaml_file
from pipelinesrc.components.data_ingestion import DataIngestion
from pipelinesrc.constants import *
import json


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys)
        

    def validate_number_of_columns(self,df:DataFrame) ->bool:
        try:
            status=len(df.columns) == len(self._schema_config["columns"])
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>status{status}")
            logging.info(f"Is required column present:[{status}]")
            return status
        except Exception as e:
            raise MyException(e,sys)
        
    def is_column_exist(self,df:DataFrame)->bool:
        try:
            dataframe_columns=df.columns
            missing_numerical_columns=[]
            missing_categorical_columns=[]
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical column:{missing_numerical_columns}")

            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)
            if len(missing_categorical_columns)>0:
                logging.info(f"Missing numerical column:{missing_categorical_columns}")
            return False if len(missing_categorical_columns)>0 or len(missing_categorical_columns)>0 else True

        except Exception as e:
            raise MyException(e,sys) from e
        
    @staticmethod
    def read_data(file_path) ->DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e,sys)
        

    def initiate_data_validation(self) ->DataValidationArtifact:

        try:
            validation_error_msf=""
            print(f">>>>>>>>>>>>>>>>>{self.data_ingestion_artifact.trained_file_path}")
            logging.info("Starting data validation")
            train_df,test_df=(DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                              DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))
            status=self.validate_number_of_columns(df=train_df)
            if not status:
                validation_error_msf+=f"Columns are missing in training datafame"
            else:
                logging.info(f"All required columns present in training dataframe:{status}")

            status=self.validate_number_of_columns(df=test_df)
            if not status:
                validation_error_msf+=f"Columns are missing in test datafame"
            else:
                logging.info(f"All required columns present in testing dataframe:{status}")
            status=self.is_column_exist(df=train_df)
            if not status:
                validation_error_msf+=f"Columns are missing in training datafame"
            else:
                logging.info(f"All categorical/int   columns present in training dataframe:{status}")

            status=self.is_column_exist(df=test_df)
            if not status:
                validation_error_msf+=f"Columns are missing in test datafame"
            else:
                logging.info(f"All categorical/int   columns present in testing dataframe:{status}")

            validation_status=len(validation_error_msf) ==0
            data_validation_artifact=DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msf,
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            )

            report_dir=os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            validation_report={
                "validation_status":validation_status,
                "message":validation_error_msf.strip()
            }

            with open(self.data_validation_config.validation_report_file_path,"w") as report_file:
                json.dump(validation_report,report_file,indent=4)
            logging.info(f"Data Validatio artifact created and saved to json file")
            logging.info(f"Data Validatio artifact::{data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise MyException(e,sys) from e
        
if __name__ == "__main__":
    ingestion=DataIngestion()
    data_arti=ingestion.initiate_data_ingestion()
    validation=DataValidation(data_ingestion_artifact=data_arti,data_validation_config=DataValidationConfig)
    validation.initiate_data_validation()