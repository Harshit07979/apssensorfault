#to define or store all the outputs
#for this project which has 6 components in trainig pipline has 6 artificat
#1. data ingestion
#2. data validation
#3. data transformation
#4. model training
#5. model evaluation
#6. model deployment or pusher
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str 
    test_file_path:str

#to store output this variable contain the report.yaml location
@dataclass
class DataValidationArtifact:
    report_file_path:str


@dataclass
class DataTransformationArtifact:
    transformed_train_path:str
    transformed_test_path:str
    transform_object_path:str
    target_encoder_path:str

@dataclass
class ModelTrainerArtifact:
    model_path:str 
    f1_train_score:float 
    f1_test_score:float

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    improved_accuracy:float

@dataclass
class ModelPusherArtifact:
    pusher_model_dir:str 
    saved_model_dir:str

