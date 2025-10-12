from networksecurity.components.data_ingestion import DataIngestion 
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation 
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging 
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig 
import sys 



if __name__ == "__main__":
  try:
    trainingpipelineconfig = TrainingPipelineConfig()
    dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
    data_ingestion = DataIngestion(dataingestionconfig)
    logging.info("Initiate the Data Ingestion")
    dataingestionartifact = data_ingestion.initiate_data_ingestion()
    print(dataingestionartifact)
    logging.info("Data Initiation Completed")
    data_validation_config = DataValidationConfig(trainingpipelineconfig)
    data_validation = DataValidation(dataingestionartifact, data_validation_config)
    logging.info("Initiating the Data Validation")
    data_validation_artifact = data_validation.initiate_data_validation()
    logging.info("Data Validation Completed")
    print(data_validation_artifact)
    data_transfomration_config = DataTransformationConfig(trainingpipelineconfig)
    data_transformation = DataTransformation(data_validation_artifact, data_transfomration_config)
    logging.info("Initiating the Data Transformation")
    data_transformation_artifact = data_transformation.initiate_data_transformation()
    print(data_transformation_artifact)
    logging.info("Data Transformation Completed")
    
  except Exception as e:
    raise NetworkSecurityException(e, sys)
  

    
