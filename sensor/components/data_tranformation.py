#now its time to transform the datas 
from importlib import simple
import os,sys
from sensor.components import data_ingestion
from sensor.entity import config_entity,artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import pandas as pd
import numpy as np
from sensor import utils
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from imblearn.combine import SMOTETomek  #to generate some data for minorty class and balance the data
from sensor.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder

class DataTransformation:

    # we need location of train and test file from artifact as input
    def __init__(self, data_transformation_config: config_entity.DataTransformationConfig, data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact 
        except Exception as e:
            raise SensorException(e, sys)

    
    # Different instances of the same class have separate memory and are isolated from each other.
    # To allow all instances to share the same data, we use a class method.
    # This method will return a shared data transformation object for every instance that calls it.
    # as it share same data we dont need to create objects we can call it by directly its name
    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        """
        This class method creates and returns a data transformation pipeline
        that includes SimpleImputer and RobustScaler.
        """
        try:
            #we will use simple imputer and robust scaler so whenever someone call pipeline it will give these two methods
            logging.info("Creating data transformer object")
            simple_imputer =SimpleImputer(strategy="constant",fill_value=0)
            robust_scaler = RobustScaler()
            #we will use pipeline to combine these two methods
            pipeline = Pipeline([("imputer",simple_imputer),("scaler",robust_scaler)])
            return pipeline
        except Exception as e:
            raise SensorException(e, sys)
        
    def initiate_data_transformation(self,)->artifact_entity.DataTransformationArtifact:
        """
        This method initiates the data transformation process which includes
        reading train and test data, transforming features, balancing the dataset,
        and saving the transformed data and objects.
        """
        try:
            #reading train and test file
            logging.info("Importing train and test file")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #now we will divide are data set further into input class and target class like xtain ytrain xtest ytest
            #we will use train_df and test_df to create xtrain ytrain xtest ytest
            logging.info("Splitting input and target feature from train and test file")
            input_feature_train_df = train_df.drop(columns=TARGET_COLUMN, axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            input_feature_test_df = test_df.drop(columns=TARGET_COLUMN, axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            #now we will encode our data
            label_encoder= LabelEncoder()
            # fitting the target class
            label_encoder.fit(target_feature_train_df)
            #transforming the target class
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            #now to call the DataTransformation
            #we will use class method to call the data transformation object
            #we will use pipeline to combine these two methods
            transformation_pipeline = DataTransformation.get_data_transformer_object()
            #we will use fit_transform to fit and transform the data
            transformation_pipeline.fit(input_feature_train_df)
            #we will use transform to transform the data which will give us output in arr
            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            #now we will balance our data usinf smttomek and increase minority daata
            smt = SMOTETomek(random_state=42)
            logging.info(f"Before Resampling in training set input:{input_feature_train_arr.shape} Taregt: {target_feature_train_arr.shape}")
            #fitting the data
            input_feature_train_arr, target_feature_train_arr=smt.fit_resample(input_feature_train_arr, target_feature_train_arr)
            logging.info(f"After Resampling in training set input:{input_feature_train_arr.shape} Target: {target_feature_train_arr.shape}")
            logging.info(f"Before Resampling in training set input:{input_feature_test_arr.shape} Taregt: {target_feature_test_arr.shape}")

            input_feature_test_arr, target_feature_test_arr=smt.fit_resample(input_feature_test_arr, target_feature_test_arr)
            logging.info(f"After Resampling in training set input:{input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")
            #transforming the data
            logging.info("Saving transformed data")

            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr ]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            #save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array=train_arr)

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array=test_arr)


            utils.save_object(file_path=self.data_transformation_config.transform_object_path, obj=transformation_pipeline)

            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
            obj=label_encoder)



            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path

            )

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
        
        except Exception as e:
            raise SensorException(e, sys)