import boto3
from pipelinesrc.configuration.aws_connection import S3Client
from io import StringIO
from typing import Union,List
import os,sys
from pipelinesrc.logger import logging
from pipelinesrc.exception import MyException
from pandas import DataFrame,read_csv
from mypy_boto3_s3.service_resource import Bucket
from pipelinesrc.constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_SECRET_ACCESS_KEY_ENV_KEY,REGION_NAME,MODEL_PUSHER_S3_KEY

import pickle

class SimpleStorageService:

    def __init__(self):
        

        s3_client=S3Client()
        self.s3_resource=s3_client.s3_resource
        self.s3_client=s3_client.s3_client
        self.s3_key=MODEL_PUSHER_S3_KEY


    def s3_key_path_available(self,bucket_name ,s3_key
                              ) ->bool:

        try:
            bucket=self.get_bucket(bucket_name)
            file_objects=[file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            print(f">>>>>>>>>>>>>>len {len(file_objects)}")
            return len(file_objects)>0
        
        except Exception as e:
            raise MyException(e,sys)
        

    @staticmethod
    def read_object(object_name:str,decode:bool=True,make_readable:bool=False) ->Union[StringIO,str]:
        try:
            func=(
                lambda:object_name.get()["Body"].read().decode()
                if decode else object_name.get()["Body"].read()

            )

            conv_func=lambda:StringIO(func()) if make_readable else func()
            return conv_func()
        except Exception as e:
            raise MyException(e,sys) from e
        

    def get_bucket(self,bucket_name:str) ->Bucket:

        logging.info("Entered the get_bucket method of simpleStorageService class")
        try:
            bucket=self.s3_resource.Bucket(bucket_name)
            logging.info("Exited the get_bucket method of SimpleStorageSerice class")
            print(f">>>>>>>>>>get_bucket{bucket}")
            return bucket
        
        except Exception as e:
            raise MyException(e,sys) from e
        


    def get_file_object(self,filename:str,bucket_name:str) ->Union[List[object],object]:

        logging.info("Entered the get_file_object method of SimpleStorageService class")
        try:
            bucket=self.get_bucket(bucket_name)
            file_objects=[file_object for file_object in bucket.objects.filter(Prefix=filename)]
            fucn=lambda x:x[0] if len(x) == 1 else x
            file_objs=fucn(file_objects)
            
            logging.info("Exited the get_file_object method of  SimpleStorageSerice class")
            return file_objs
        except Exception as e:
            raise MyException(e,sys) from e
        


    def load_model(self,model_name:str,bucket_name:str,model_dir:str=None) ->object:

        try:
            model_file=model_dir + "/" + model_name if model_dir else model_name
            file_object=self.get_file_object(model_file,bucket_name)
            model_obj=self.read_object(file_object,decode=False)
            model=pickle.loads(model_obj)
            logging.info("Production model loaded from s3 bucket")
            return model
        except Exception as e:
            raise MyException(e,sys) from e
        

    def upload_file(self,from_filename:str,to_filename:str,bucket_name:str,remove:bool=True):

        try:
            logging.info(f"Uploading {from_filename} to {to_filename} in {bucket_name}")
            self.s3_resource.meta.client.upload_file(from_filename,bucket_name,to_filename)
            logging.info(f"Uploaded {from_filename} to {to_filename} i {bucket_name}")

            if remove:
                os.remove(from_filename)
                logging.info(f"Removed local file {from_filename} after upload")
            logging.info("Exited the upload_file method of simplestorageservice class")
        except Exception as e:
            raise MyException(e,sys) from e
        


# storage=SimpleStorageService()
# b_n=storage.get_bucket(bucket_name="model-mlops-proj")
# storage.read_object(object_name="model.pkl")