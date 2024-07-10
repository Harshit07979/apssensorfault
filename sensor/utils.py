import os
import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import  sys
import yaml

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description:
    Read data from collection as dataframe
    =======================================
    parameters
    :param database_name: name of the database
    :param collection_name: name of the collection
    :return: dataframe
    ==============================================
    return as pandas dataframe

    """
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df= pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping columns: _id")
            df=df.drop("_id",axis=1)
        logging.info(f"Row and columns")
        return df
    except Exception as e:
        raise SensorException(e, sys)

#to get report in yaml form of datavlidation we will define a function here
def write_yaml_file(file_path,data:dict):
    try:
        #first we will create director for it
        file_dir=os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise SensorException(e, sys)
    
#converting object columns into float of data validation in initiatedatavalidation
def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                df[column]=df[column].astype(float)
        return df
                
    except Exception as e:
        raise SensorException(e, sys)
