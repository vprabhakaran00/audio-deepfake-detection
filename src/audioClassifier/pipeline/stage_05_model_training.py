from audioClassifier.config.configuration import ConfigManager
from audioClassifier.components.callback_preparation import CallbackPreparation
from audioClassifier.components.model_training import ModelTraining
from audioClassifier import logger

STAGE_NAME = "Model Training Stage"

class ModelTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigManager()
        callback_preparation_config = config.read_callback_prep_config()
        callback_preparation = CallbackPreparation(config = callback_preparation_config)
        prepared_callbacks = callback_preparation.prepare_callbacks()
        
        model_training_config = config.read_model_train_config()
        model_training = ModelTraining(config = model_training_config)
        model_training.train_model(callback = prepared_callbacks)   
        
if __name__ == '__main__':
    try:
        logger.info(f">>>>>>> {STAGE_NAME} started <<<<<<<")
        pipe = ModelTrainingPipeline()
        pipe.main()
        logger.info(f">>>>>>> {STAGE_NAME} completed <<<<<<<\n\n====================")
    except Exception as e:
        logger.exception(e)
        raise e