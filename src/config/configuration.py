from src.constants import *
from src.utils.common import read_yaml, create_directories
from src.entity.config_entity import (DataIngestionConfig)

class ConfigurationManager:
    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            FOLDER_ID_NP=config.FOLDER_ID_NP,
            FOLDER_ID_P=config.FOLDER_ID_P,
            DOWNLOAD_PATH_NP=config.DOWNLOAD_PATH_NP,
            DOWNLOAD_PATH_P=config.DOWNLOAD_PATH_P,
            CREDENTIALS_FILE=config.CREDENTIALS_FILE
        )
        return data_ingestion_config