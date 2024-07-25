import os
from audioClassifier.constants import *
from audioClassifier.utils.common import open_yaml_file, create_directories
from audioClassifier.entity.config_entity import (DataIngestionConfig, DataTransformationConfig, DataValidationConfig, 
                                                  ModelPreparationConfig, CallbackPreparationConfig, ModelTrainingConfig)

class ConfigManager:
    def __init__(self, config_file = CONFIG_PATH, params_file = PARAMS_PATH):
        self.config = open_yaml_file(config_file)
        self.params = open_yaml_file(params_file)
        
        create_directories([self.config.artifacts_root])
        
        
    def read_data_ingestion_config(self) -> DataIngestionConfig:
        data_ingestion = self.config.data_ingestion
        
        create_directories([self.config.data_ingestion.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir = Path(data_ingestion.root_dir),
            source_URL = data_ingestion.source_URL,
            local_data_file = Path(data_ingestion.local_data_file),
            unzip_dir = Path(data_ingestion.unzip_dir)
        )
        
        return data_ingestion_config
    
    
    def read_data_trans_config(self) -> DataTransformationConfig:
        data_trans = self.config.data_transformation
        
        create_directories([self.config.data_transformation.root_dir])
        
        data_trans_config = DataTransformationConfig(
            root_dir = Path(data_trans.root_dir),
            data_path = Path(data_trans.data_path),
            n_fft = data_trans.n_fft,
            hop_length = data_trans.hop_length,
            n_mels = data_trans.n_mels 
        )
        
        return data_trans_config
    
    
    def read_data_val_config(self) -> DataValidationConfig:
        data_val = self.config.data_validation
        
        create_directories([self.config.data_validation.root_dir])
        
        data_val_config = DataValidationConfig(
            root_dir = Path(data_val.root_dir),
            data_path = Path(data_val.data_path),
            status_file = Path(data_val.status_file),
            required_files = data_val.required_files
        )
        
        return data_val_config
    
    
    def read_model_prep_config(self) -> ModelPreparationConfig:
        model_prep = self.config.model_preparation
        
        create_directories([self.config.model_preparation.root_dir])
        
        model_prep_config = ModelPreparationConfig(
            root_dir = Path(model_prep.root_dir),
            base_model_path = Path(model_prep.base_model_path),
            updated_model_path = Path(model_prep.updated_model_path)
        )
        
        return model_prep_config
    
    
    def read_callback_prep_config(self) -> CallbackPreparationConfig:
        callback_prep = self.config.callback_preparation
        
        checkpoint_dir = os.path.dirname(callback_prep.model_checkpoint_dir)
        create_directories([checkpoint_dir, self.config.callback_preparation.tensorboard_log_dir])
        
        callback_prep_config = CallbackPreparationConfig(
            root_dir = Path(callback_prep.root_dir),
            tensorboard_log_dir = Path(callback_prep.tensorboard_log_dir),
            model_checkpoint_dir = Path(callback_prep.model_checkpoint_dir),
            early_stopping_monitor = self.params.early_stopping_monitor,
            early_stopping_patience = self.params.early_stopping_patience 
        )
        
        return callback_prep_config
    
    
    def read_model_train_config(self) -> ModelTrainingConfig:
        model_train = self.config.model_training
        model_prep = self.config.model_preparation
        data_val = self.config.data_validation
        
        create_directories([self.config.model_training.root_dir])
        
        model_train_config = ModelTrainingConfig(
            root_dir = Path(model_train.root_dir),
            trained_model_dir = Path(model_train.trained_model_dir),
            data_dir = Path(data_val.data_path),
            updated_model_dir = Path(model_prep.updated_model_path),
            metrics = self.params.metrics,
            batch_size = self.params.batch_size,
            epochs = self.params.epochs,   
            learning_rate = self.params.learning_rate
        )
        
        return model_train_config