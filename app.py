from pipelinesrc.data_access.data_mongo import Proj1Data
from pipelinesrc.constants import DB_NAME,COLLLECTION_NAME
from pipelinesrc.configuration.mongo_db_connection import MongoDBClient





proj1=Proj1Data()
proj1.export_collection_as_datafrome(collection_name=COLLLECTION_NAME)
print(proj1)


# mongo_client=MongoDBClient(database_name=DB_NAME)
# print(mongo_client.database)