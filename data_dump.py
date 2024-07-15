#it is used to loaded data from github using wget and then convert it into json format and load it into mongo db
import pymongo
import pandas as pd
import json
from dotenv import load_dotenv

print(f"Loading environment variable from .env file")
load_dotenv()

#from sensor.config import mongo_client

#prividing link to mongodb local host
client =pymongo.MongoClient("mongodb+srv://harshit00709:DUOlJBEak0k7pXKh@cluster01.jrh9fuf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01")

#giving name to my datafram to store in mongodb
DATA_FILE_PATH="E:/sensordetect/aps_failure_training_set1.csv"
DATABASE_NAME="apsdata"
COLLECTION_NAME="sensordata"

#loading data from csv file into dataframe

if __name__=="__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")

    #Convert dataframe to json so that we can dump these record in mongo db
    df.reset_index(drop=True,inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])
    #insert converted json record to mongo db
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)