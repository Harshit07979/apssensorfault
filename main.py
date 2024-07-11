import os
import sys
from sensor.components import data_tranformation
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity import config_entity
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_tranformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer

from sensor.pipeline import training_pipeline
from sensor.utils import get_collection_as_dataframe

file_path = "E:/sensordetect/aps_failure_training_set1.csv"
print(__name__)

if __name__ == "__main__":
    try:
        #data ingestion
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        print(data_ingestion.initiate_data_ingestion)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        #data validation
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)

        #data transformation
        data_transformation_config =config_entity.DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config, data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()

        #model trainig
        model_trainer_config = config_entity.ModelTrainingConfig(training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        print("model_trained")

    except Exception as e:
        print(e)
