from audioClassifier.config.configuration import ConfigManager
from audioClassifier.components.model_preparation import ModelPreparation
from audioClassifier import logger

STAGE_NAME = "Model Preparation Stage"

class ModelPreparationTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigManager()
        model_preparation_config = config.read_model_prep_config()
        model_preparation = ModelPreparation(config = model_preparation_config)
        model_preparation.build_full_model()
        
if __name__ == '__main__':
    try:
        logger.info(f">>>>>>> {STAGE_NAME} started <<<<<<<")
        pipe = ModelPreparationTrainingPipeline()
        pipe.main()
        logger.info(f">>>>>>> {STAGE_NAME} completed <<<<<<<\n\n====================")
    except Exception as e:
        logger.exception(e)
        raise e