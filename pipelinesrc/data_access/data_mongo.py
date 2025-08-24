import sys
import pandas as pd
import numpy as np
from typing import Optional
from pipelinesrc.constants import DB_NAME,COLLLECTION_NAME
from pipelinesrc.exception import MyException
# from pipelinesrc.configuration.mongo_db_connection import MongoDBClient
from pipelinesrc.configuration.mongo_db_connection import MongoDBClient

class Proj1Data:

    def __init__(self) ->None:
        try:

            self.mongo_client=MongoDBClient(database_name=DB_NAME)
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>self.mongo{self.mongo_client}")
           
        except Exception as e:
            raise MyException(e,sys)
    

    def export_collection_as_datafrome(self,collection_name:str,database_name:Optional[str] =None) ->pd.DataFrame:

        try:
            if database_name is None:
                collection=self.mongo_client.database[collection_name]
                # collection=self.mongo_client[collection_name]
            else:
                collection=self.mongo_client[database_name][collection_name]

            print(f"Fetching data from mongoDB")
            df=pd.DataFrame(list(collection.find()))
            print(f"Data fetched with len::{len(df)}")
            if "id" in df.columns.to_list():
                df=df.drop(columns=["id"],axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise MyException(e,sys)