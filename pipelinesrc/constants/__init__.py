import os
from datetime import date

DB_NAME="insurance"
COLLLECTION_NAME="insurance-cluster"
MONGODB_URL_KEY="mongodb+srv://mdsohailahmed711:pxQ9Kb7IM75Y3UQR@insurance-cluster.pmwhhkz.mongodb.net/?retryWrites=true&w=majority&appName=insurance-cluster"


ARTIFACT_DIR:str= "artifact"
PIPELINE_NAME:str=""

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


