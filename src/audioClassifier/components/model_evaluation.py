import numpy as np
from tensorflow.keras.models import load_model
from audioClassifier import logger
from audioClassifier.entity.config_entity import ModelEvaluationConfig
from audioClassifier.utils.common import write_to_json


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
        
    def _load_val_data(self):
        try:
            X_test = np.load(self.config.data_dir / 'X_test.npy')
            y_test = np.load(self.config.data_dir / 'y_test.npy')
            return X_test, y_test
        except Exception as e:
            logger.error(f"Error loading validation data: {e}")
            raise e
    
    def _load_trained_model(self):
        try:
            model = load_model(str(self.config.trained_model_dir))
            return model
        except Exception as e:
            logger.error(f"Error loading the trained model: {e}")
            raise e
        
    def _parse_metrics(self, metrics_list):
        parsed_metrics = ['loss'] + metrics_list
        return parsed_metrics
    
    def evaluate_model(self):
        X_test, y_test = self._load_val_data()
        model = self._load_trained_model()
        metrics_list = self._parse_metrics(self.config.metrics)
        
        try:
            score = model.evaluate(X_test, y_test)
            eval_scores = dict(zip(metrics_list, score))
            write_to_json(eval_scores, self.config.evaluation_results_dir)
            logger.info(f"Model evaluated successfully and results saved to {self.config.evaluation_results_dir}.")
        except Exception as e:
            logger.error(f"Error evaluating the model: {e}")
            raise e