import sys
import pandas as pd
import numpy as np
from typing import Optional
from pipelinesrc.constants import DB_NAME,COLLLECTION_NAME
from pipelinesrc.exception import MyException
# from pipelinesrc.configuration.mongo_db_connection import MongoDBClient
from pipelinesrc.configuration.mongo_db_connection import MongoDBClient
# from pymongoarrow.api import find_pandas_all

class Proj1Data:

    def __init__(self) ->None:
        try:

            self.mongo_client=MongoDBClient(database_name=DB_NAME)
            # print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>self.mongo{self.mongo_client}")
           
        except Exception as e:
            raise MyException(e,sys)
    

    def export_collection_as_datafrome(self,collection_name:str,database_name:Optional[str] =None) ->pd.DataFrame:

        try:
            if database_name is None:
                collection=self.mongo_client.database[collection_name]
                # collection=self.mongo_client[collection_name]
            else:
                collection=self.mongo_client[database_name][collection_name]
            print("Fetching data from MOnoDB")

            # print(len(list(collection.find())))
            total_documents = collection.count_documents({})
            # for data in range(0,total_documents,20000):
                # print(data)
            print(total_documents)
            curosr=collection.find().limit(10000)
            print("Fetching data from mongoDB")
            df = pd.DataFrame(list(curosr))
            print(f"Data fecthed with len: {len(df)}")
            if "id" in df.columns.to_list():
                df = df.drop(columns=["id"], axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise MyException(e,sys)
        
# data=Proj1Data()
# print(data.export_collection_as_datafrome(collection_name="insurance-cluster"))