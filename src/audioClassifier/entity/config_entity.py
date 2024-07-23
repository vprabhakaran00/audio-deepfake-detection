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
    status_file: str
    required_files: list
    
@dataclass(frozen=True)
class ModelPreparationConfig:
    root_dir: Path
    base_model_path: Path
    updated_model_path: int
    metrics: list
    learning_rate: float