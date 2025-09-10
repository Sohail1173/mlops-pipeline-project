import boto3
from pipelinesrc.constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_SECRET_ACCESS_KEY_ENV_KEY,REGION_NAME,MODEL_PUSHER_S3_KEY


_aws_access_key_id=AWS_ACCESS_KEY_ID_ENV_KEY
_aws_secret_key_id=AWS_SECRET_ACCESS_KEY_ENV_KEY
s3 = boto3.resource('s3',aws_access_key_id=_aws_access_key_id,
                    aws_secret_access_key=_aws_secret_key_id,
                                                region_name=REGION_NAME)

# Initialize the S3 resource
# s3 = boto3.resource('s3')

# Get the specific S3 bucket
bucket_name = 'model-mlops-proj'  # Replace with your bucket name
bucket = s3.Bucket(bucket_name)

# Define the prefix to filter by
prefix = 'model'  # Replace with your desired prefix (e.g., 'images/', 'data/logs/')

# Filter objects using the prefix
filtered_objects = bucket.objects.filter(Prefix=MODEL_PUSHER_S3_KEY)


# Iterate and print the keys of the filtered objects
for obj in filtered_objects:
    print(obj.key)