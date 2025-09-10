import os
from datetime import date
from dotenv import load_dotenv
from pipelinesrc.constants import *
load_dotenv()



DB_NAME="insurance"
COLLLECTION_NAME="insurance-cluster-01"
MONGODB_URL_KEY=os.getenv("MONGODB_URL_KEY")

ARTIFACT_DIR:str= "artifact"
PIPELINE_NAME:str=""

TARGET_COLUMN = "Response"

DATA_INGESTION_COLLECTION_NAME: str = "insurance-cluster"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.25

FILE_NAME: str = "data.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")


DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_REPORT_FILE_NAME:str="report.yaml"


DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str="transformed_object"

PREPROCESSING_OBJECT_FILE_NAME="preprocessing.pkl"


MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")
MODEL_TRAINER_N_ESTIMATORS=200
MODEL_TRAINER_MIN_SAMPLES_SPLIT: int = 7
MODEL_TRAINER_MIN_SAMPLES_LEAF: int = 6
MIN_SAMPLES_SPLIT_MAX_DEPTH: int = 10
MIN_SAMPLES_SPLIT_CRITERION: str = 'entropy'
MIN_SAMPLES_SPLIT_RANDOM_STATE: int = 101

MODEL_FILE_NAME = "model.pkl"


# -AWS_ACCESS_KEY_ID_ENV_KEY = os.getenv("AWS_ACCESS_KEY_ID_ENV_KEY")
# AWS_SECRET_ACCESS_KEY_ENV_KEY =os.getenv("AWS_SECRET_ACCESS_KEY_ENV_KEY")
# REGION_NAME = "us-east-1"

AWS_ACCESS_KEY_ID_ENV_KEY = os.getenv("AWS_ACCESS_KEY_ID_ENV_KEY")
AWS_SECRET_ACCESS_KEY_ENV_KEY = os.getenv("AWS_SECRET_ACCESS_KEY_ENV_KEY")
REGION_NAME = "us-east-1"



MODEL_EVALUATIO_CHANGED_THRESHOLD_SCORE:float=0.02

MODEL_BUCKET_NAME="model-mlops-proj"
MODEL_PUSHER_S3_KEY="model"
# z/"model_registry"


APP_HOST = "0.0.0.0"
APP_PORT = 5000




