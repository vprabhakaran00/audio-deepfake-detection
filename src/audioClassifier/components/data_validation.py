import os
from audioClassifier import logger
from audioClassifier.entity.config_entity import DataValidationConfig


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
        
    def validate_data(self) -> None:
        try:
            val_status = None
            with open(self.config.status_file, 'w') as f:
                for file in os.listdir(self.config.data_path):
                    if file in self.config.required_files:
                        val_status = 'Pass'
                        f.write(f"Validation Status of '{file}': {val_status}\n")
                    else:
                        val_status = 'Fail'
                        f.write(f"Validation Status of '{file}': {val_status}\n")
        except Exception as e:
            logger.error(f"Error occured when validating data files: {e}.")