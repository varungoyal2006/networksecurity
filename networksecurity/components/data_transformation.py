import sys, os 
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging 
import pandas as pd 
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline 

from networksecurity.constant.training_pipeline import TARGET_COLUMN 
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS 

from networksecurity.entity.artifact_entity import DataTransformationArtifacts, DataValidationArtifact

from networksecurity.entity.config_entity import DataTransformationConfig 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging 

from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_objects 

class DataTransformation:
  def __init__(self, data_validation_artifact: DataValidationArtifact, 
  data_transformation_config:
  DataTransformationConfig):
    try :
      self.data_validation_artifact:DataValidationArtifact = data_validation_artifact 
      self.data_transformation_config : DataTransformationConfig = data_transformation_config 
    except Exception as e:
      raise NetworkSecurityException(e, sys)
  
  @staticmethod 
  def read_data(file_path) -> pd.DataFrame:   
    try:
      return pd.read_csv(file_path)
    except Exception as e:
      raise NetworkSecurityException(e, sys)
  
  def get_data_transformer_object(cls) -> Pipeline:
    logging.info("Enteredt the get_data_transformer_object method of Data_Transformation class")
    try : 
      imputer : KNNImputer =  KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
      logging.info(f"Initialized the KNNImputer with the following parameters : {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
      preprocessor : Pipeline = Pipeline(steps = [("imputer", imputer)])
      logging.info("Created the preprocessing object")
      return preprocessor 

    except Exception as e:
      raise NetworkSecurityException(e, sys)
  def initiate_data_transformation(self) -> DataTransformationArtifacts:
    try:
      logging.info("Entered the initiate_data_transformation method of Data_Transformation class")
      train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
      test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
      logging.info("Read the train and test data as dataframe")

      ## Traning dataframe 
      input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis = 1)
      target_feature_train_df = train_df[TARGET_COLUMN].replace(-1, 0)

      ## Testing dataframe 
      input_feature_test_df = test_df.drop(columns = [TARGET_COLUMN], axis = 1)
      target_feature_test_df = test_df[TARGET_COLUMN].replace(-1, 0)

      preprocessor_object = self.get_data_transformer_object()
      logging.info("Obtained the preprocessor object")

      preprocessor_object.fit(input_feature_train_df)
      transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
      transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

      logging.info("Transformed the training and testing input features")
      
      train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
      test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]
      
      #saving the numpy array data 
      save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array = train_arr)
      save_numpy_array_data(self.data_transformation_config.tranformed_test_file_path, array = test_arr)
      save_objects(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

      logging.info("Saved the transformed training and testing array")

      # Preparing the artifacts 
      data_transfomration_artifact = DataTransformationArtifacts(
        transformed_train_file_path = self.data_transformation_config.transformed_train_file_path, 
        transformed_test_file_path = self.data_transformation_config.tranformed_test_file_path,
        transformed_object_file_path = self.data_transformation_config.transformed_object_file_path  

      )
      return data_transfomration_artifact

    except Exception as e:
      raise NetworkSecurityException(e, sys)