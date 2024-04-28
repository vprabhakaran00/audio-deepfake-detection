from audioClassifier import logger
from audioClassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from audioClassifier.pipeline.stage_02_data_transformation import DataTransformationTrainingPipeline
from audioClassifier.pipeline.stage_03_data_validation import DataValidationTrainingPipeline

STAGE_NAME = 'Data Ingestion Stage'

try:
    logger.info(f">>>>>>> {STAGE_NAME} started <<<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>>> {STAGE_NAME} completed <<<<<<<\n\n====================")
except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = 'Data Loading and Transformation Stage'

try:
    logger.info(f">>>>>>> {STAGE_NAME} started <<<<<<<")
    data_transform = DataTransformationTrainingPipeline()
    data_transform.main()
    logger.info(f">>>>>>> {STAGE_NAME} completed <<<<<<<\n\n====================")
except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = 'Data Validation Stage'

try:
    logger.info(f">>>>>>> {STAGE_NAME} started <<<<<<<")
    data_transform = DataValidationTrainingPipeline()
    data_transform.main()
    logger.info(f">>>>>>> {STAGE_NAME} completed <<<<<<<\n\n====================")
except Exception as e:
    logger.exception(e)
    raise e