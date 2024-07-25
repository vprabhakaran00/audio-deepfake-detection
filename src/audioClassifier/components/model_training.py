import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import AUC, Precision, Recall, TruePositives, TrueNegatives, FalsePositives, FalseNegatives
from audioClassifier import logger
from pathlib import Path
from audioClassifier.entity.config_entity import ModelTrainingConfig


class ModelTraining:
    def __init__(self, config: ModelTrainingConfig):
        self.config = config
        
    def _load_data(self):
        try:
            X_train = np.load(self.config.data_dir / 'X_train.npy')
            y_train = np.load(self.config.data_dir / 'y_train.npy')
            X_test = np.load(self.config.data_dir / 'X_test.npy')
            y_test = np.load(self.config.data_dir / 'y_test.npy')
            return X_train, y_train, X_test, y_test
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise e
        
    def _parse_metrics(self, metrics_list):
        parsed_metrics = []
        for metric in metrics_list:
            if metric == 'accuracy':
                parsed_metrics.append('accuracy')
            elif metric == 'auc':
                parsed_metrics.append(AUC(name = 'auc'))
            elif metric == 'recall':
                parsed_metrics.append(Recall(name = 'recall'))
            elif metric == 'precision':
                parsed_metrics.append(Precision(name = 'precision'))
            elif metric == 'true_positives':
                parsed_metrics.append(TruePositives(name = 'true_positives'))
            elif metric == 'true_negatives':
                parsed_metrics.append(TrueNegatives(name = 'true_negatives'))
            elif metric == 'false_positives':
                parsed_metrics.append(FalsePositives(name = 'false_positives'))
            elif metric == 'false_negatives':
                parsed_metrics.append(FalseNegatives(name = 'false_negatives'))
            else:
                raise ValueError(f"Unsupported metric: {metric}")
        return parsed_metrics
    
    def _load_model(self):
        try:
            model = load_model(str(self.config.updated_model_dir), compile = False)
            metrics_list = self._parse_metrics(self.config.metrics)
            model.compile(optimizer = Adam(learning_rate = self.config.learning_rate), 
                              loss = 'binary_crossentropy', 
                              metrics = metrics_list)
            return model
        except Exception as e:
            logger.error(f"Error loading and compiling model: {e}")
            raise e
    
    def train_model(self, callback: list):
        X_train, y_train, X_test, y_test = self._load_data()
        model = self._load_model()
        
        try:
            model.fit(X_train, y_train, epochs = self.config.epochs, batch_size = self.config.batch_size, validation_data = [X_test, y_test], callbacks = callback)
            model.save(str(self.config.trained_model_dir))
            logger.info(f"Model trained successfully and saved to {self.config.trained_model_dir}.")
        except Exception as e:
            logger.error(f"Error training the model: {e}")
            raise e