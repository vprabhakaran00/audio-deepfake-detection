from audioClassifier.config.configuration import ConfigManager
from audioClassifier.components.data_validation import DataValidation
from audioClassifier import logger

STAGE_NAME = "Data Validation Stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigManager()
        data_validation_config = config.read_data_val_config()
        data_validation = DataValidation(config = data_validation_config)
        data_validation.validate_data()
        
if __name__ == '__main__':
    try:
        logger.info(f">>>>>>> {STAGE_NAME} started <<<<<<<")
        pipe = DataValidationTrainingPipeline()
        pipe.main()
        logger.info(f">>>>>>> {STAGE_NAME} completed <<<<<<<\n\n====================")
    except Exception as e:
        logger.exception(e)
        raise e