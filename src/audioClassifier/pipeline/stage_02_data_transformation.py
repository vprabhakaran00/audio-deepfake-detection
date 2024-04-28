from audioClassifier.config.configuration import ConfigManager
from audioClassifier.components.data_transformation import DataTransformation
from audioClassifier import logger

STAGE_NAME = "Data Loading and Transformation Stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigManager()
        data_transformation_config = config.read_data_trans_config()
        data_transformation = DataTransformation(config = data_transformation_config)
        data_transformation.load_data()
        
if __name__ == '__main__':
    try:
        logger.info(f">>>>>>> {STAGE_NAME} started <<<<<<<")
        pipe = DataTransformationTrainingPipeline()
        pipe.main()
        logger.info(f">>>>>>> {STAGE_NAME} completed <<<<<<<\n\n====================")
    except Exception as e:
        logger.exception(e)
        raise e