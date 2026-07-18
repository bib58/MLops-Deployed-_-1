from dotenv import load_dotenv
load_dotenv()
import os
from dataclasses import dataclass
from datetime import datetime

BUCKET = os.getenv("S3_bucket")
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = "acchiPipe"
    artifact_dir:str = os.path.join("artifact", TIMESTAMP)
    timestamp: str = TIMESTAMP

training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")
    feature_store_file_path: str = os.path.join(data_ingestion_dir, "feature_store", "data.csv")
    training_file_path: str = os.path.join(data_ingestion_dir, "ingested", "train.csv")
    testing_file_path: str = os.path.join(data_ingestion_dir, "ingested", "test.csv")
    train_test_split_ratio: float = 0.25
    collection_name: str = os.getenv("COLLECTION_NAME")

@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, "data_validation")
    validation_report_file_path: str = os.path.join(data_validation_dir, "report.yaml")

@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, "data_transformation")
    transformed_train_file_path: str = os.path.join(data_transformation_dir, "transformed", "train.csv".replace("csv", "npy"))
    transformed_test_file_path: str = os.path.join(data_transformation_dir, "transformed", "test.csv".replace("csv", "npy"))
    transformed_object_file_path: str = os.path.join(data_transformation_dir, "transformed_object", "preprocess.pkl")

@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, "model_trainer")
    trained_model_file_path: str = os.path.join(model_trainer_dir, "trained_model", "model.pkl")
    expected_accuracy: float = 0.6
    model_config_file_path: str = os.path.join("config", "model.yaml")
    _n_estimators = 200
    _min_samples_split = 7
    _min_samples_leaf = 6
    _max_depth = 10
    _criterion = 'entropy'
    _random_state = 101

@dataclass
class ModelEvaluationConfig:
    changed_threshold_score: float = 0.02
    bucket_name: str = BUCKET
    s3_model_key_path: str = "model.pkl"

@dataclass
class ModelPusherConfig:
    bucket_name: str = BUCKET
    s3_model_key_path: str = "model.pkl"

@dataclass
class VehiclePredictorConfig:
    model_bucket_name: str = BUCKET
    model_file_path: str = "model.pkl"