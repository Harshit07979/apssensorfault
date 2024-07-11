#input dir has been  created iin config entity and its location has been stored in artifact entity
#now we will check for missing values and drop it check data drift check required columns 

import os,sys
from sensor.entity import config_entity,artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging

from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
from sensor import utils
from typing import Optional
from sensor import utils
from sensor.config import TARGET_COLUMN

class DataValidation:
    logging.info(f"Class Datavalidation IS accesed")

    def __init__(self,
                    data_validation_config:config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        logging.info(f"Class DataVAlidation has Been accesed")
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config=data_validation_config
            #to read train and test data file which directory and output can be read from dataingestion artifact
            self.data_ingestion_artifact=data_ingestion_artifact
            self.validation_error=dict()
        except Exception as e:
            raise SensorException(e,sys)
        

        

        #dropping missing columns having more than 70%missing values it will take df read it find missing values and drop the columns
        #it will be used in initiate_data_validation function to drop missing values
    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
            """
            Description:
            This method is used to drop the columns having more  missing values than specified threshold
            Args:
            df: Dataframe
            threshold: Threshold value to drop the columns
            ===========================================================================================
            Returns:
            pd.Datafram or can return null values

            """
            try:
                #taking the threshold valued defind in config_entity from data validation config
                threshold=self.data_validation_config.missing_threshold
                #reading missing values columns name
                null_report=df.isna().sum()/df.shape[0]
                logging.info(f"Null report: {null_report}")
                #selectiong columns name having more than threshold missinf values
                drop_column_names=null_report[null_report>threshold].index
                #it will contain the all dropped columns name in dictionary

                self.validation_error[report_key_name]=list(drop_column_names)
                logging.info(f"Drop columns: list{drop_column_names}")
                df.drop(list(drop_column_names), axis=1,inplace=True)

                #return NOne if no columns left
                if len(df.columns)==0:
                    return None
                return df
            except Exception as e:
                raise SensorException(e,sys)
            
            #to tcheck required columns are avaialable in datasets are not
    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
            try:
                base_columns=base_df.columns
                current_columns=current_df.columns
                missing_columns = []
                for base_column in base_columns:
                    if base_column not in current_columns:
                        logging.info(f"Column: [{base_column} is not available.]")
                        missing_columns.append(base_column)
                    
                
            
                if len(missing_columns)>0:
                    self.validation_error[report_key_name]=missing_columns
                    return False
                return True
            except Exception as e:
                raise SensorException(e,sys)
            
    #checking change in data and preparing a report is having same distribution or not
    def data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, report_key_name: str):
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns
            for base_column in base_columns:
                base_data, current_data = base_df[base_column], current_df[base_column]

            # Handle missing values
                base_data = base_data.dropna()
                current_data = current_data.dropna()
            

                if base_data.empty or current_data.empty:
                    logging.warning(f"Column {base_column} has no data after dropping missing values.")
                    drift_report[base_column] = {"pvalues": float('nan'), "same_distribution": False}
                    continue

            # Ensure data types are consistent
                if base_data.dtype != current_data.dtype:
                    logging.warning(f"Column {base_column} has inconsistent data types: {base_data.dtype} vs {current_data.dtype}")
                    drift_report[base_column] = {"pvalues": float('nan'), "same_distribution": False}
                    continue

            # Perform KS test
                same_distribution = ks_2samp(base_data, current_data)
                pvalue = same_distribution.pvalue
                if pvalue > 0.05:
                # we are accepting null hypothesis
                    drift_report[base_column] = {"pvalues": float(pvalue), "same_distribution": True}
                else:
                    drift_report[base_column] = {"pvalues": float(pvalue), "same_distribution": False}
                
                logging.info(f"Column: {base_column}, pvalue: {pvalue}, same_distribution: {drift_report[base_column]['same_distribution']}")

            self.validation_error[report_key_name] = drift_report
        
        except Exception as e:
            raise SensorException(e, sys)
    
        

        




    # 
    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.nan},inplace=True)
            logging.info(f"Replace na value in base df")
            #base_df has na as null
            #droppign missing values usinf missing_values_columns function
            logging.info(f"Drop null values colums from base df")
            base_df=self.drop_missing_values_columns(df=base_df,report_key_name="missing_values_within_base_dataset")

            #readind train and test df from dataingestion artifact
            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #dropping null values from train and test dataset
            logging.info(f"Drop null values colums from train df")
            train_df = self.drop_missing_values_columns(df=train_df,report_key_name="missing_values_within_train_dataset")
            logging.info(f"Drop null values colums from test df")
            test_df = self.drop_missing_values_columns(df=test_df,report_key_name="missing_values_within_test_dataset")
            

            exclude_columns = [TARGET_COLUMN]
            base_df = utils.convert_columns_float(df=base_df, exclude_columns=exclude_columns)
            train_df = utils.convert_columns_float(df=train_df, exclude_columns=exclude_columns)
            test_df = utils.convert_columns_float(df=test_df, exclude_columns=exclude_columns)

            #now check is required coumns exist in both dataset or not
            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")
            
            #if only both above are true only then we can go for data drift status
            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=test_df,report_key_name="data_drift_within_test_dataset")

            #write the report
            logging.info("Write reprt in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)

