from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import l2
from audioClassifier import logger
from pathlib import Path
from audioClassifier.entity.config_entity import ModelPreparationConfig


class ModelPreparation:
    def __init__(self, config: ModelPreparationConfig):
        self.config = config
        
    def _build_base_model(self):
        try:
            base_model = MobileNetV3Large(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
            for layer in base_model.layers:
                layer.trainable = False
            base_model.save(self.config.base_model_path)
            logger.info(f"MobileNetV3Large Base Model built successfully and saved to {self.config.base_model_path}.")
            return base_model
        except Exception as e:
            logger.error(f"Error building and saving base model: {e}")
            raise e
    
    def build_full_model(self):
        try:
            upd_model = Sequential([
                self._build_base_model(),
                Flatten(),
                Dropout(0.5),
                Dense(32, activation='relu', kernel_regularizer=l2(0.01)),
                Dense(1, activation = 'sigmoid')
            ])
            upd_model.summary()
            upd_model.save(self.config.updated_model_path)
            logger.info(f"Updated Model compiled and saved to {self.config.updated_model_path}.")
        except Exception as e:
            logger.error(f"Error building and compiling updated model: {e}")
            raise e