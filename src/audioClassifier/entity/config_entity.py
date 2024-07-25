from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
    
@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    n_fft: int
    hop_length: int
    n_mels: int
    
@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    data_path: Path
    status_file: Path
    required_files: list
    
@dataclass(frozen=True)
class ModelPreparationConfig:
    root_dir: Path
    base_model_path: Path
    updated_model_path: Path
    
@dataclass(frozen=True)
class CallbackPreparationConfig:
    root_dir: Path
    tensorboard_log_dir: Path
    model_checkpoint_dir: Path
    early_stopping_monitor: str
    early_stopping_patience: int
    
@dataclass(frozen=True)
class ModelTrainingConfig:
    root_dir: Path
    trained_model_dir: Path
    data_dir: Path
    updated_model_dir: Path
    metrics: list
    epochs: int
    batch_size: int
    learning_rate: float