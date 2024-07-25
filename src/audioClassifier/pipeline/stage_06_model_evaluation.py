from audioClassifier.config.configuration import ConfigManager
from audioClassifier.components.model_evaluation import ModelEvaluation
from audioClassifier import logger

STAGE_NAME = "Model Evaluation Stage"

class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigManager()
        model_evaluation_config = config.read_model_eval_config()
        model_evaluation = ModelEvaluation(config = model_evaluation_config)
        model_evaluation.evaluate_model()
        
if __name__ == '__main__':
    try:
        logger.info(f">>>>>>> {STAGE_NAME} started <<<<<<<")
        pipe = ModelEvaluationTrainingPipeline()
        pipe.main()
        logger.info(f">>>>>>> {STAGE_NAME} completed <<<<<<<\n\n====================")
    except Exception as e:
        logger.exception(e)
        raise e