import os 
import sys 
import json
import certifi 
import pandas as pd 
import pymongo 

from dotenv import load_dotenv 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")  # Corrected spelling
print(MONGO_DB_URL)

ca = certifi.where()  # Certificate authority file for secure connection


class NetworkDataExtract():
    def __init__(self):
        try:
            # Initialize Mongo client
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
  
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            # Convert each row to a dictionary
            records = data.to_dict(orient="records")
            return records 
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def insert_data_mongodb(self, records, database_name, collection_name):
        try:
            database = self.mongo_client[database_name]
            collection = database[collection_name]

            # Insert records into MongoDB
            collection.insert_many(records)
            return len(records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    try:
        FILE_PATH = "Network_Data/phisingData.csv"   # ✅ corrected spelling
        DATABASE = "VARUNAI"
        COLLECTION = "NetworkData"

        networkobj = NetworkDataExtract()

        records = networkobj.csv_to_json_converter(FILE_PATH)
        print(f"Sample record: {records[0]}")  # print one sample row

        no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
        print(f"✅ Successfully inserted {no_of_records} records into MongoDB")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
