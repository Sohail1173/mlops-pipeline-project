import os
import sys
import pandas as pd
import numpy as np
from pandas import DataFrame
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.compose import ColumnTransformer
from pipelinesrc.constants import *
from pipelinesrc.entity.config_entity import DataTransformationCofig,DataIngestionConfig,DataValidationConfig
from pipelinesrc.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact,DataValidationArtifact
from pipelinesrc.exception import MyException
from pipelinesrc.logger import logging
from pipelinesrc.utils.main_utils import save_object,save_numpy_array_data,read_yaml_file
from pipelinesrc.components.data_ingestion import DataIngestion
from pipelinesrc.components.data_validation import DataValidation


class DataTrasformation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_transformation_config:DataTransformationCofig,
                 data_validation_artifact:DataValidationArtifact):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact
            self._schema_config=read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys)
        

    @staticmethod
    def read_data(file_path) ->DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e,sys)
        

    def get_data_transformer_object(self) ->Pipeline:

        logging.info("Entered transformation method")
        try:
            numerical_transformer=StandardScaler()
            min_max_scalar=MinMaxScaler()
            logging.info("Transformers Initialized:StandardScaler")
            num_feature=self._schema_config["num_features"]
            mm_columns=self._schema_config["mm_columns"]
            logging.info("Cols loaded from schema")

            preprocessor = ColumnTransformer(
                transformers=[
                    ("StandardScaler", numerical_transformer, num_feature),
                    ("MinMaxScaler", min_max_scalar, mm_columns)
                ],
                remainder='passthrough'  
            )
            print(f">>>>>>>>Preprocessor get_data_transormer::{preprocessor}")

            final_pipeline=Pipeline(steps=[("Preprocessor",preprocessor)])
            logging.info("Final Pipeline Ready")
            logging.info("Exited data transformation method")
            return final_pipeline
        except Exception as e:
            logging.exception("Exception occured in data transformation method")
            raise MyException(e,sys)
        
    def _map_gender_column(self,df):
        logging.info("Mapping 'Gender' column to binary values")
        df["Gender"]=df["Gender"].map({"Female":0,"Male":1}).astype(int)
        return df
    

    def _create_dummy_columns(self,df):
        logging.info("Creating dummy variables for categorical features")
        df=pd.get_dummies(df,drop_first=True)
        return df
    
    def _rename_columns(self,df):
        logging.info("Renaming specific columns ad casting to int")
        df=df.rename(columns={
            "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_< 2 Year": "Vehicle_Age_lt_1_Year",
        })

        for col in ["Vehicle_Age_it_1_Year","Vehicle_Age_gt_2_Years","Vehicle_Damage_Yes"]:
            if col in df.columns:
                df[col]=df[col].astype('int')
        return df
    

    def _drop_id_columns(self,df):
        logging.info("Dropping id colums")
        drop_col=self._schema_config["drop_columns"]
        if drop_col in df.columns:
            df=df.drop(drop_col,axis=1)
        return df
    

    def intiate_data_transformation(self) ->DataTransformationArtifact:

        try:
            logging.info("Data Transformation started ")
            # rep_train_file_path=self.data_transformation_config.transformed_train_file_path
            # rep_test_file_path=self.data_transformation_config.transformed_test_file_path
            # print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{rep_train_file_path}")
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_ingestion_artifact.message)
            tran_df=self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df=self.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            logging.info("Train-Test data loaded")

            input_feature_train_df=tran_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=tran_df[TARGET_COLUMN]
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            logging.info("Input and Target cols defined for both train and test df")

            input_feature_train_df=self._map_gender_column(input_feature_train_df)
            input_feature_train_df=self._drop_id_columns(input_feature_train_df)
            input_feature_train_df=self._create_dummy_columns(input_feature_train_df)
            input_feature_train_df=self._rename_columns(input_feature_train_df)

            input_feature_test_df=self._map_gender_column(input_feature_test_df)
            input_feature_test_df=self._drop_id_columns(input_feature_test_df)
            input_feature_test_df=self._create_dummy_columns(input_feature_test_df)
            input_feature_test_df=self._rename_columns(input_feature_test_df)
            logging.info("Custom transformatios applied to train and test data")

            logging.info("Starting data transformation")
            preporcessor=self.get_data_transformer_object()
            logging.info("Got the preprocessor object")


            logging.info("Initializing transformation for training-data")
            # preporcessor.fit(input_feature_train_df)
            input_feature_train_arr=preporcessor.fit_transform(input_feature_train_df)
            logging.info("Initializing transformation for testing-data")
            # preporcessor.fit(input_feature_train_df)
            input_feature_test_arr=preporcessor.fit_transform(input_feature_test_df)


            logging.info("Applying SMOTEEN for handling imbalance dataset")
            smt=SMOTEENN(sampling_strategy="minority")
            input_feature_train_final,target_feature_train_final=smt.fit_resample(
                input_feature_train_arr,target_feature_train_df
            )
            input_feature_test_final,target_feature_test_final=smt.fit_resample(
                input_feature_test_arr,target_feature_test_df
            )

            logging.info("SMOTEEN applied to train-test df")

            train_arr=np.c_[input_feature_train_final,np.array(target_feature_train_final)]
            test_arr=np.c_[input_feature_test_final,np.array(target_feature_test_final)]
            logging.info("feature-target concat done for traina and test df")


            # print(f">>>>>>>>>self.data_transformation_config.transformed_train_file_path{self.data_transformation_config.transformed_train_file_path}")
            

            save_object(self.data_transformation_config.transformed_object_file_path,preporcessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            logging.info("Saving transformation object and trasformed files")



            logging.info("Data transformation completed successfully")
            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                # transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_train_file_path
            )
        
        except Exception as e:
            raise MyException(e,sys) from e
 