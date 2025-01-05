from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class DataIngestionConfig:
    root_dir: Path
    FOLDER_ID_NP: str
    FOLDER_ID_P: List[str]
    DOWNLOAD_PATH_NP: Path
    DOWNLOAD_PATH_P: Path
    CREDENTIALS_FILE: Path