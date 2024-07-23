from audioClassifier.constants import *
from audioClassifier.utils.common import open_yaml_file, create_directories
from audioClassifier.entity.config_entity import (DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelPreparationConfig)

class ConfigManager:
    def __init__(self, config_file = CONFIG_PATH, params_file = PARAMS_PATH):
        self.config = open_yaml_file(config_file)
        self.params = open_yaml_file(params_file)
        
        create_directories([self.config.artifacts_root])
        
        
    def read_data_ingestion_config(self) -> DataIngestionConfig:
        data_ingestion = self.config.data_ingestion
        
        create_directories([self.config.data_ingestion.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir = data_ingestion.root_dir,
            source_URL = data_ingestion.source_URL,
            local_data_file = data_ingestion.local_data_file,
            unzip_dir = data_ingestion.unzip_dir
        )
        
        return data_ingestion_config
    
    
    def read_data_trans_config(self) -> DataTransformationConfig:
        data_trans = self.config.data_transformation
        
        create_directories([self.config.data_transformation.root_dir])
        
        data_trans_config = DataTransformationConfig(
            root_dir = data_trans.root_dir,
            data_path = data_trans.data_path,
            n_fft = data_trans.n_fft,
            hop_length = data_trans.hop_length,
            n_mels = data_trans.n_mels 
        )
        
        return data_trans_config
    
    
    def read_data_val_config(self) -> DataValidationConfig:
        data_val = self.config.data_validation
        
        create_directories([self.config.data_validation.root_dir])
        
        data_val_config = DataValidationConfig(
            root_dir = data_val.root_dir,
            data_path = data_val.data_path,
            status_file = data_val.status_file,
            required_files = data_val.required_files
        )
        
        return data_val_config
    
    
    def read_model_prep_config(self) -> ModelPreparationConfig:
        model_prep = self.config.model_preparation
        
        create_directories([self.config.model_preparation.root_dir])
        
        model_prep_config = ModelPreparationConfig(
            root_dir = model_prep.root_dir,
            base_model_path = model_prep.base_model_path,
            updated_model_path = model_prep.updated_model_path,
            metrics = self.params.metrics,
            learning_rate = self.params.learning_rate   
        )
        
        return model_prep_config