import sys
from pipelinesrc.cloud_storage.aws_storage import SimpleStorageService
from pipelinesrc.exception import MyException
from pipelinesrc.logger import logging
from pipelinesrc.entity.artifact_entity import ModelPusherArtifact,ModelEvaluatioArtifact
from pipelinesrc.entity.config_entity import ModelPusheConfig
from pipelinesrc.entity.s3_estimator import Proj1Estimator


class ModelPusher:
    def __init__(self,model_evaluation_artifact:ModelEvaluatioArtifact,
                 model_pusher_config:ModelPusheConfig):
        self.s3=SimpleStorageService()
        self.model_evaluation_artifact=model_evaluation_artifact
        self.model_pusher_config=model_pusher_config,
        self.proj1_estimator=Proj1Estimator(bucket_name=model_pusher_config.bucket_name,
                                            model_path=model_pusher_config.s3_model_key_path)
        


    def intiate_model_pusher(self) ->ModelPusherArtifact:

        try:
            logging.info("Uploading artifact folder to s3 bucket")
            logging.info("Uploading new model to s3 bucket...")
            self.proj1_estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)
            model_pusher_artifact=ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,
                                                      s3_model_path=self.model_pusher_config.s3_model_key_path)
            
            logging.info("Uploaded artifact folder to s3 bucket")
            logging.info(f"Model pusher artifact:{model_pusher_artifact}")
            logging.info("Exoted intiate_model_pusher method of ModelTrainer class")
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e,sys)
        

