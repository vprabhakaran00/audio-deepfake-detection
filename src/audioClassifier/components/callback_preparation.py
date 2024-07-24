import time
import os
from tensorflow.keras import callbacks
from audioClassifier import logger
from audioClassifier.entity.config_entity import CallbackPreparationConfig

class CallbackPreparation:
    def __init__(self, config: CallbackPreparationConfig):
        self.config = config
        
    def _get_timestamped_tb_directory(self):
        timestamp = time.strftime("%Y-%m-%d--%H:%M:%S")
        return os.path.join(self.config.tensorboard_log_dir, f"run-{timestamp}")
    
    def prepare_callbacks(self):
        tensorboard_log_dir = self._get_timestamped_tb_directory()
        
        try:
            tensorboard_callback = callbacks.TensorBoard(log_dir = tensorboard_log_dir)
            checkpoint_callback = callbacks.ModelCheckpoint(filepath = self.config.model_checkpoint_path, 
                                                            save_best_only = True)
            early_stopping_callback = callbacks.EarlyStopping(monitor = self.config.early_stopping_monitor, 
                                                              patience = self.config.early_stopping_patience, 
                                                              restore_best_weights = True)
            return [tensorboard_callback, checkpoint_callback, early_stopping_callback]
        except Exception as e:
            logger.error(f"Error creating callbacks: {e}")
            raise e