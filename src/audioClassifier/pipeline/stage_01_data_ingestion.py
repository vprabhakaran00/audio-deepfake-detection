from audioClassifier.config.configuration import ConfigManager
from audioClassifier.components.data_ingestion import DataIngestion
from audioClassifier import logger

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigManager()
        data_ingestion_config = config.read_data_ingestion_config()
        data_ingestion = DataIngestion(config = data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_file()

        
if __name__ == '__main__':
    try:
        logger.info(f">>>>>>> {STAGE_NAME} started <<<<<<<")
        pipe = DataIngestionTrainingPipeline()
        pipe.main()
        logger.info(f">>>>>>> {STAGE_NAME} completed <<<<<<<\n\n====================")
    except Exception as e:
        logger.exception(e)
        raise e