#to define all the input which is also called configuration to use it in other files like components subfiles
#for this project which has 6 components in trainig pipline
#1. data ingestion
#2. data validation
#3. data transformation
#4. model training
#5. model evaluation
#6. model deployment or pusher

import os
from datetime import datetime
import sys
from sensor.exception import SensorException
from sensor.logger import logging


from sensor.exception import SensorException

FILE_NAME="sensor.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"


#to store every input ouutput in trainig pipeline each and eavery file in single folder
class TrainingPipelineConfig:


    def __init__(self):
        """
        initialise the class
        it will create the the folder name artifact with time stamps
        whenever we run the program new output will be created in artifact which will later store in data_ingestion file
        """
        self.artifact_dir=os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")

#(:...) means pass
class DataIngestionConfig:
    """
        Description:
        it will create data ingestion file inside artifact with database name and colllection
        it will create the folder name artifact with time stamps
        =========================================================
        Parameters
        :param training_pipeline_config: it will take the artifact folder name
        :param feature_store_file_path: it will take the artifact folder name with feature_store folder in artifact
        :param train_file_path: it will take the artifact folder name with train_file_path
        :param test_file_path: it will take the artifact folder name with test_file_path
        :param test_size: it will take the artifact folder name with test_size
        =========================================================
        return
        :return: it will return the path of artifact folder subfolder

        """

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        
        self.database_name="apsdata"
        self.collection_name="sensordata"
        self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
        self.train_file_path=os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
        self.test_file_path=os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
        self.test_size=0.2 #to split data into train and test in component.data_ingestion_py file
    
    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise SensorException(e, sys)




class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainingConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...

