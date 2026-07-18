import os
import sys
import pymongo
import certifi
from src.exception import MyException
from src.logger import logging
from dotenv import load_dotenv
load_dotenv()

# certifi is used to provide a trusted CA (Certificate Authority) certificate bundle for verifying SSL/TLS certificates when connecting to MongoDB Atlas.
ca = certifi.where()

class MongoDBClient:
    client = None 
    def __init__(self, database_name: str = None) -> None:
        try:
            if database_name is None:
                database_name = os.getenv("DATABASE_NAME")
                if database_name is None:
                    raise Exception("Environment variable 'DATABASE_NAME' is not set.")

            if MongoDBClient.client is None:
                mongo_db_url = os.getenv("MONGODB_URL")
                if mongo_db_url is None:
                    raise Exception("Environment variable 'MONGODB_URL' is not set.")
                
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
                
            self.client = MongoDBClient.client
            self.database = self.client[database_name] 
            self.database_name = database_name
            logging.info("MongoDB connection successful.")
            
        except Exception as e:
            raise MyException(e, sys)