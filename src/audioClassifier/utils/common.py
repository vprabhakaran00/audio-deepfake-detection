import os
from box.exceptions import BoxValueError
import yaml
from audioClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def open_yaml_file(file_path: Path) -> ConfigBox:
    """
    Reads a YAML file and returns a ConfigBox object.
    
    Args:
        filepath (Path): The path to the YAML file.
    
    Returns:
        ConfigBox: YAML content as a ConfigBox object.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        BoxValueError: If the file is empty.
        yaml.YAMLError: If there is an error reading the file.
    """
    try:
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
            if yaml_data is None:
                raise BoxValueError("Error: File is empty.")
            logger.info(f"YAML file '{file_path}' was loaded successfully.")
            return ConfigBox(yaml_data)
    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
        return None
    except yaml.YAMLError as e:
        logger.error(f"Error reading YAML file: '{file_path}': {e}")
        return None
    except BoxValueError as e:
        logger.error(e)
        return None
    
@ensure_annotations
def create_directories(paths: list):
    """
    Creates directories for the given list of paths if they don't already exist.

    Args:
        paths (list): List of paths to create directories
        
    Raises:
        OSError: If there is an error creating any of the directories.
    """
    for path in paths:
        try:
            os.makedirs(path, exist_ok = True)
            logger.info(f"Directory '{path}' created successfully or already exists.")
        except OSError as e:
            logger.error(f"Error creating directory '{path}': {e}")
            raise
    
@ensure_annotations
def write_to_json(data: dict, path: Path):
    """
    Writes data to JSON file

    Args:
        data (dict): Data to be written to JSON file.
        path (Path): Path to the JSON file.
    
    Raises:
        Exception: IF there is an error writing to the file.
    """
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent = 4)
        logger.info(f"Data successfully written and saved to JSON file: '{path}'.")
    except Exception as e:
        logger.exception(f"Error writing data to JSON file: '{path}': {e}")
        raise
    
@ensure_annotations
def get_file_size(file_path: Path) -> str:
    """
    Gets the size of a file in kilobytes.

    Args:
        file_path (Path): The path to the file.

    Returns:
        str: The size of the file in KB.
    """
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            size_in_kb = round(os.path.getsize(file_path)/1024, 2)
            return f" - {size_in_kb} KB"
        else:
            logger.error(f"File {file_path} not found or is not a regular file.")
            return None
    except Exception as e:
        logger.exception(f"Error getting file size from file '{file_path}': {e}")
        return None      