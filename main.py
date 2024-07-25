from audioClassifier import logger
from audioClassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from audioClassifier.pipeline.stage_02_data_transformation import DataTransformationTrainingPipeline
from audioClassifier.pipeline.stage_03_data_validation import DataValidationTrainingPipeline
from audioClassifier.pipeline.stage_04_model_preparation import ModelPreparationTrainingPipeline
from audioClassifier.pipeline.stage_05_model_training import ModelTrainingPipeline

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
    data_validation = DataValidationTrainingPipeline()
    data_validation.main()
    logger.info(f">>>>>>> {STAGE_NAME} completed <<<<<<<\n\n====================")
except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = 'Model Preparation Stage'

try:
    logger.info(f">>>>>>> {STAGE_NAME} started <<<<<<<")
    model_preparation = ModelPreparationTrainingPipeline()
    model_preparation.main()
    logger.info(f">>>>>>> {STAGE_NAME} completed <<<<<<<\n\n====================")
except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = 'Model Training Stage'

try:
    logger.info(f">>>>>>> {STAGE_NAME} started <<<<<<<")
    model_preparation = ModelTrainingPipeline()
    model_preparation.main()
    logger.info(f">>>>>>> {STAGE_NAME} completed <<<<<<<\n\n====================")
except Exception as e:
    logger.exception(e)
    raise e