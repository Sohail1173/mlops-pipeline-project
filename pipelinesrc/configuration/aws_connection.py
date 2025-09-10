import boto3
import os
from pipelinesrc.constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_SECRET_ACCESS_KEY_ENV_KEY,REGION_NAME
# import bot

class S3Client:

    s3_client=None
    s3_resource=None

    def __init__(self,region_name=REGION_NAME):
        
        if S3Client.s3_resource==None or S3Client.s3_client==None:

            _access_key_id=AWS_ACCESS_KEY_ID_ENV_KEY
            _secret_access_key=AWS_SECRET_ACCESS_KEY_ENV_KEY

        
            
            S3Client.s3_resource=boto3.resource('s3',
                                                aws_access_key_id=_access_key_id,
                                                aws_secret_access_key=_secret_access_key,
                                                region_name=region_name)
            S3Client.s3_client=boto3.client('s3',
                                            aws_access_key_id=_access_key_id,
                                            aws_secret_access_key=_secret_access_key,
                                            region_name=region_name)
            
        self.s3_resource=S3Client.s3_resource
        self.s3_client=S3Client.s3_client
        print(f">>>>>>>>>>>>>>>>s3_resource::{self.s3_resource}")
        print(f">>>>>>>>>>>>>>>>s3_client::{self.s3_client}")

# aws=S3Client()