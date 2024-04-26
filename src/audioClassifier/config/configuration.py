from audioClassifier.constants import *
from audioClassifier.utils.common import open_yaml_file, create_directories
from audioClassifier.entity.config_entity import DataIngestionConfig

class ConfigManager:
    def __init__(self, config_file = CONFIG_PATH, params_file = PARAMS_PATH):
        self.config = open_yaml_file(config_file)
        self.params = open_yaml_file(params_file)
        
        create_directories([self.config.artifacts_root])
        create_directories([self.config.data_ingestion.root_dir])
        
    def read_data_ingestion_config(self) -> DataIngestionConfig:
        data_ingestion = self.config.data_ingestion
        
        data_ingestion_config = DataIngestionConfig(
            root_dir = data_ingestion.root_dir,
            source_URL = data_ingestion.source_URL,
            local_data_file = data_ingestion.local_data_file,
            unzip_dir = data_ingestion.unzip_dir
        )
        
        return data_ingestion_config