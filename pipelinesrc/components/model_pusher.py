import sys
from pipelinesrc.cloud_storage.aws_storage import SimpleStorageService
from pipelinesrc.exception import MyException
from pipelinesrc.logger import logging
# from pipelinesrc.entity.artifact_entity import ModelPusherArtifact,ModelEvaluatioArtifact
from pipelinesrc.entity.config_entity import ModelPusheConfig
from pipelinesrc.entity.s3_estimator import Proj1Estimator
from pipelinesrc.entity.artifact_entity  import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluatioArtifact,ModelPusherArtifact
from pipelinesrc.entity.config_entity  import ModelTrainerConfig,DataIngestionConfig,DataTransformationCofig,DataValidationConfig,ModelEvaluationConfig,ModelPusheConfig
from pipelinesrc.exception import MyException
from pipelinesrc.logger import logging
from pipelinesrc.components.data_ingestion import DataIngestion
from pipelinesrc.components.data_validation import DataValidation
from pipelinesrc.components.data_transformation import DataTrasformation
from pipelinesrc.components.model_evaluation import ModelEvaluation
from pipelinesrc.components.model_trainer import ModelTrainer


class ModelPusher:
    def __init__(self,model_evaluation_artifact:ModelEvaluatioArtifact,
                 model_pusher_config:ModelPusheConfig):
        self.s3=SimpleStorageService()
        self.model_evaluation_artifact=model_evaluation_artifact
        self.model_pusher_config=model_pusher_config
        self.proj1_estimator=Proj1Estimator(bucket_name=model_pusher_config.bucket_name,
                                            model_path=model_pusher_config.s3_model_key_path)
        


    def intiate_model_pusher(self) ->ModelPusherArtifact:

        try:
            logging.info("Uploading artifact folder to s3 bucket")
            logging.info("Uploading new model to s3 bucket...")
            self.proj1_estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)
            model_pusher_artifact=ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,
                # bucket_name=ModelPusheConfig.bucket_name,
                                                      s3_model_path=self.model_pusher_config.s3_model_key_path
                                                      )
            
            logging.info("Uploaded artifact folder to s3 bucket")
            logging.info(f"Model pusher artifact:{model_pusher_artifact}")
            logging.info("Exoted intiate_model_pusher method of ModelTrainer class")
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e,sys)
        

# if __name__ == "__main__":
#     ingestion=DataIngestion()
#     data_arti=ingestion.initiate_data_ingestion()
#     validation=DataValidation(data_ingestion_artifact=data_arti,data_validation_config=DataValidationConfig)
#     data_vali=validation.initiate_data_validation()
#     data_trans=DataTrasformation(data_ingestion_artifact=data_arti,data_validation_artifact=data_vali,data_transformation_config=DataTransformationCofig)
#     data_trans=data_trans.intiate_data_transformation()
#     trainer=ModelTrainer(data_transformation_artifact=data_trans,model_trainer_config=ModelTrainerConfig)
#     model_tra=trainer.intiate_model_trainer()
#     model_eval=ModelEvaluation(model_eval_config=ModelEvaluationConfig,data_ingestion_artifact=data_arti,model_trainer_artifact=model_tra)
#     eval=model_eval.initiate_model_evaluation()


#     pusher=ModelPusher(model_evaluation_artifact=eval,
#                        model_pusher_config=ModelPusheConfig)
#     pusher.intiate_model_pusher()