#to define all the input which is also called configuration to use it in other files like components subfiles
#for this project which has 6 components in trainig pipline
#1. data ingestion
#2. data validation
#3. data transformation
#4. model training
#5. model evaluation
#6. model deployment or pusher

# #to store every input ouutput in trainig pipeline each and eavery file in single folder
# class TrainingPipelineConfig:

#     def __init__(self):
#        
#         initialise the class
#         it will create the the folder name artifact with time stamps
#         whenever we run the program new output will be created in artifact which will later store in data_ingestion file
#        
# class DataIngestionConfig:
#     """
#         Description:
#         it will create data ingestion file inside artifact with database name and colllection
#         it will create the folder name artifact with time stamps
#         =========================================================
#         Parameters
#         :param training_pipeline_config: it will take the artifact folder name
#         :param feature_store_file_path: it will take the artifact folder name with feature_store folder in artifact
#         :param train_file_path: it will take the artifact folder name with train_file_path
#         :param test_file_path: it will take the artifact folder name with test_file_path
#         :param test_size: it will take the artifact folder name with test_size
#         =========================================================
#         return
#         :return: it will return the path of artifact folder subfolder

#         """




import os
from datetime import datetime
import sys
from sensor.exception import SensorException
from sensor.logger import logging

FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME="tranformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME="target_encoder.pkl"
MODEL_FILE_NAME="model.pkl"

class TrainingPipelineConfig:
    """
    Configuration class for the Training Pipeline.

    This class is responsible for initializing the directory structure where all 
    artifacts related to the training pipeline will be stored. It creates a unique 
    directory based on the current timestamp to ensure that each run of the pipeline 
    has its own separate set of outputs.

    Attributes:
        artifact_dir (str): Path to the directory where all pipeline artifacts will be stored.
    """
    def __init__(self):
        """
        Initializes the TrainingPipelineConfig class.

        This method creates a directory named 'artifact' in the current working 
        directory, appending a timestamp to ensure uniqueness.
        """
        self.artifact_dir = os.path.join(
            os.getcwd(), "artifact", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}"
        )


class DataIngestionConfig:
    """
    Configuration class for the Data Ingestion component.

    This class sets up the configuration required for data ingestion, including 
    the paths for the feature store, training, and testing datasets. It also 
    specifies the database and collection names for storing ingested data.

    Attributes:
        database_name (str): Name of the database to use for data ingestion.
        collection_name (str): Name of the collection within the database.
        data_ingestion_dir (str): Directory path for data ingestion artifacts.
        feature_store_file_path (str): Path to the feature store file.
        train_file_path (str): Path to the training dataset file.
        test_file_path (str): Path to the testing dataset file.
        test_size (float): Proportion of the dataset to include in the test split.
    """
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Initializes the DataIngestionConfig class.

        Args:
            training_pipeline_config (TrainingPipelineConfig): Configuration object for the training pipeline.

        This method sets up various paths and parameters needed for data ingestion, 
        including database and collection names, and paths to feature store, training, 
        and testing datasets.
        """
        self.database_name = "apsdata"
        self.collection_name = "sensordata"
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir, "data_ingestion"
        )
        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir, "feature_store", FILE_NAME
        )
        self.train_file_path = os.path.join(
            self.data_ingestion_dir, "dataset", TRAIN_FILE_NAME
        )
        self.test_file_path = os.path.join(
            self.data_ingestion_dir, "dataset", TEST_FILE_NAME
        )
        self.test_size = 0.2  # Proportion of the dataset to include in the test split

    def to_dict(self) -> dict:
        """
        Converts the DataIngestionConfig object attributes to a dictionary.

        Returns:
            dict: A dictionary representation of the DataIngestionConfig object's attributes.
        
        Raises:
            SensorException: If there is an error during the conversion.
        """
        try:
            return self.__dict__
        except Exception as e:
            raise SensorException(e, sys)



#it will check the distribution of dataa whether same or not after splitting data 
class DataValidationConfig:
     
    #creaating directory in artifact where subdir is data validation in the path obtained by artifact dir
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(
            training_pipeline_config.artifact_dir, "data_validation"
        )

    #now we will create report.yaml file in artifacr dir under data valiidatin usinf path derivsed from data validation dir
        self.report_file_path=os.path.join(self.data_validation_dir,"report.yaml")
        self.missing_threshold:float=0.7
        #using base csv file to validate later
        self.base_file_path=os.path.join("E:/sensordetect/aps_failure_training_set1.csv")

        #now input dir has been created now we have to write output and store it in this input dir report.yaml
        #also we need to import input which we will do in components

    



#we will use robust scaler due to outliers and simple imputers to fill missing values with mean also we need to do data balancing
#we need to store transfered train and test data and use it later to train model
class DataTransformationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir , "data_transformation")
        self.transform_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)
        self.transformed_train_path =  os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_NAME.replace("csv","npz"))
        self.transformed_test_path =os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_NAME.replace("csv","npz"))
        self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)


class ModelTrainingConfig:

     def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir , "model_trainer")
        self.model_path = os.path.join(self.model_trainer_dir,"model",MODEL_FILE_NAME)
        self.expected_score = 0.7
        self.overfitting_threshold = 0.1
class ModelEvaluationConfig:...
class ModelPusherConfig:...

