import os
import sys
from pandas import DataFrame
import pandas as pd
from pipelinesrc.entity.artifact_entity  import(DataIngestionArtifact,DataValidationArtifact,
                                                DataTransformationArtifact,ModelTrainerArtifact,
                                                ModelEvaluatioArtifact,ModelPusherArtifact)
from pipelinesrc.entity.config_entity  import(ModelTrainerConfig,DataIngestionConfig,
                                              DataTransformationCofig,DataValidationConfig,ModelEvaluationConfig,ModelPusheConfig)
from pipelinesrc.exception import MyException
from pipelinesrc.logger import logging
from pipelinesrc.components.data_ingestion import DataIngestion
from pipelinesrc.components.data_validation import DataValidation
from pipelinesrc.components.data_transformation import DataTrasformation
from pipelinesrc.components.model_trainer import ModelTrainer
from pipelinesrc.components.model_evaluation import ModelEvaluation
from pipelinesrc.components.model_pusher import ModelPusher

from pipelinesrc.entity.estimator import MyModel
from pipelinesrc.constants import *
import json
import numpy as np
from typing import Optional



class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.data_validation_config=DataValidationConfig()
        self.data_transformation_config=DataTransformationCofig()
        self.model_trainer_config=ModelTrainerConfig()
        self.model_pusher_config=ModelPusheConfig()
        self.model_evaluation_config=ModelEvaluationConfig()



    def start_data_ingestion(self) ->DataIngestionArtifact:

        try:
            logging.info("Entered the start_data_ingestion method")
            logging.info("Data from mongodb")
            data_ingestion=DataIngestion()
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("Exited the data ingestion pipeline")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) ->DataValidationArtifact:

        try:
            logging.info("Entered the start_data_validation method")
            
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                           data_validation_config=self.data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("Exited the data validation pipeline")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        


    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact,
        data_validation_artifact:DataValidationArtifact) ->DataTransformationArtifact:

        try:
            logging.info("Entered the start_data_transformation method")
            
            data_transformation=DataTrasformation(data_ingestion_artifact=data_ingestion_artifact,
                                           data_validation_artifact=data_validation_artifact,
                                           data_transformation_config=self.data_transformation_config)
            data_transformation_artifact=data_transformation.intiate_data_transformation()
            logging.info("Exited the data transformation pipeline")
            return data_transformation_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact) ->ModelTrainerArtifact:

        try:
            logging.info("Entered the start_model_trainer method")
            
            model_trainer=ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                           model_trainer_config=self.model_trainer_config)
            model_trainer_artifact=model_trainer.intiate_model_trainer()
            logging.info("Exited the model_trainer pipeline")
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        

    def start_model_evaluation(self,data_ingestion_artifact:DataIngestionArtifact,
       model_trainer_artifact:ModelEvaluatioArtifact) ->ModelEvaluatioArtifact:

        try:
            logging.info("Entered the start_model_evaluation method")
            
            model_evaluation=ModelEvaluation(data_ingestion_artifact=data_ingestion_artifact,
                                             model_trainer_artifact=model_trainer_artifact,
                                             model_eval_config=self.model_evaluation_config)
            model_evaluation_artifact=model_evaluation.initiate_model_evaluation()
            logging.info("Exited the model_evaluation pipeline")
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        

    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluatioArtifact) ->ModelPusherArtifact:

        try:
            logging.info("Entered the start_model_pusher method")
            
            model_pusher=ModelPusher(model_evaluation_artifact=model_evaluation_artifact,
                                             
                                             model_pusher_config=self.model_pusher_config)
            model_pusher_artifact=model_pusher.intiate_model_pusher()
            logging.info("Exited the model_pusher pipeline")
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        


    def run_pipeline(self,) ->None:

        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(
            data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact
            )
            model_trainer_artifact=self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact
            )
            model_evaluation_artifact=self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
            model_trainer_artifact=model_trainer_artifact)
            if not model_evaluation_artifact.is_model_accepted:
                logging.info(f"Model is accepted in training pipeline")
                return None
            model_pusher_artifact=self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact,
                                                          )
        except Exception as e:
            raise MyException(e,sys)
        
if __name__ == "__main__":
    pipeline=TrainPipeline()
    pipeline.run_pipeline()
        

    
        

    