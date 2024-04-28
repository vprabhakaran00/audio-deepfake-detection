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
    sampling_rate: int
    n_fft: int
    max_length: int
    
@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    data_path: Path
    status_file: str
    required_files: list