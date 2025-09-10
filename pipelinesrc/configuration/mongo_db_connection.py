import sys
import pandas as pd
import numpy as np
import os
import certifi
import pymongo
from typing import Optional
from pipelinesrc.constants import DB_NAME,MONGODB_URL_KEY
from pipelinesrc.exception import MyException
from pipelinesrc.logger import logging
from dotenv import load_dotenv
load_dotenv()

ca=certifi.where()

class MongoDBClient:
    
    client=None

    def __init__(self,database_name:str=DB_NAME) ->None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url=os.getenv("MONGODB_URL_KEY")
                
                if mongo_db_url is None:
                    raise Exception(f"{MONGODB_URL_KEY} is not set in env")
                MongoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)

            self.client=MongoDBClient.client
            # print(f"client>>>>>>>>>>>>>>>>>>>{self.client}")
            self.database=self.client[database_name]
            self.database_name=database_name
            logging.info("MongoDB connection successful")
        except Exception as e:
            raise MyException(e,sys)
        
mon=MongoDBClient()
