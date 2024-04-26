import os
import urllib.request as request
import zipfile
from audioClassifier import logger
from audioClassifier.utils.common import get_file_size
from audioClassifier.entity.config_entity import DataIngestionConfig
from pathlib import Path

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        
    def download_file(self):
        try:
            if not os.path.exists(self.config.local_data_file):
                self._retrieve_file()
            else:
                logger.info(f"File already exists of size: {get_file_size(Path(self.config.local_data_file))}")
        except Exception as e:
            logger.error(f"Error occurred during file download: {e}")
              
    def extract_file(self):
        try:
            path = self.config.unzip_dir
            os.makedirs(path, exist_ok=True)
            self._extract_zip_file(path)
        except Exception as e:
            logger.error(f"Error occurred during file extraction: {e}")
            
    def _retrieve_file(self):
        filename, headers = request.urlretrieve(
            url=self.config.source_URL,
            filename=self.config.local_data_file
        )
        logger.info(f"Downloaded {filename} with the following info:\n{headers}")

    def _extract_zip_file(self, path: Path):
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_file:
            zip_file.extractall(path)
            logger.info(f"Extracted file '{self.config.local_data_file}' to {path}")