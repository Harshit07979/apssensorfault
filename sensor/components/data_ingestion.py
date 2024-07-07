#there is six components in ML training pipeline ---ingestion,validation,transformation,evaluation,trainer,pusher
#ingestion is the process of getting data into the system splitting the data handling na values and storing them into different files
#validation is the process of splitting the data into training and testing data and using it to validate later
#transformation is the process of cleaning the data and making it ready for training
#evaluation is the process of evaluating the model and making it ready for production
#trainer is the process of training the model and making it ready for production
#pusher is the process of pushing the model to production and making it ready for use

from sensor import utils
from sensor.entity import config_entity
from sensor.entity import artifact_entity 
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

#loading csv file and doing some changes and perfoming all the necessary task of data ingestion
class Dataingestion:

    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)
        
    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            #Exporting collection data as pandas dataframe using config_entity DataIngestionConfig class database and collection_name
            df:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name)

            logging.info("Save data in feature store")

            #now replace na values which is present in .csv file
            df.replace(to_replace="na", value=np.NAN, inplace=True)

            #now we want to store it in feature store path
            #Save data in feature store
            logging.info("Create feature store folder if not available")
            #Create feature store folder if not available  using feature store file path from config_entity DataingestionConfig class
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            logging.info("Save df to feature store folder")
            #Save df to feature store folder using feature store file path from config_entity DataingestionConfig class
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            #splitting the data into train and test
            logging.info("split dataset into train and test set")
            #split dataset into train and test set using test size from config_entity DataIngestionConfig class
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)

            #now we want to store this spliited data
            logging.info("create dataset directory folder if not available")
            #create dataset directory folder if not available
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)
            logging.info("Save df to feature store folder")
            #Save df to feature store folder using train and test file path from config_entity DataingestionConfig class
            #Save df to feature store folder
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)

            #Prepare artifact or say output which can be done using feature store file path
            #Prepare artifact using train and test file path to store seprately


            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e:
            raise SensorException(error_message=e, error_detail=sys)





