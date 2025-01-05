import os
import pathway as pw
from google.oauth2.service_account import Credentials as ServiceCredentials
from src.entity.config_entity import (DataIngestionConfig)
from pathlib import Path

class DataIngestion: 
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initialize_gdrive_client(self):
        """Initialize the Google Drive client."""
        credentials = ServiceCredentials.from_service_account_file(str(self.config.CREDENTIALS_FILE))
        client = pw.io.gdrive._GDriveClient(
            credentials=credentials
        )
        return client

    def download_pdfs_from_folder(self, folder_id: str, download_path: Path):
        """Download PDF files from a specific Google Drive folder."""
        try:
            download_path = Path(download_path)
            gdrive_client = self.initialize_gdrive_client()
            

            os.makedirs(download_path, exist_ok=True)
            pdf_files = gdrive_client._ls(folder_id)
            

            for file in pdf_files:
                file_id = file['id']
                file_name = file['name']
                file_path = download_path / file_name
                file_content = gdrive_client.download(file)
                
                if file_content:
                    with open(file_path, 'wb') as f:
                        f.write(file_content)
                    print(f"Downloaded: {file_name}")
                else:
                    print(f"Failed to download: {file_name}")
        except Exception as e:
            print(f"Error downloading files from folder {folder_id}: {e}")
            raise e

    def download(self):
        """Download PDFs from both non-publishable and publishable folders."""
        try:
            self.download_pdfs_from_folder(self.config.FOLDER_ID_NP, self.config.DOWNLOAD_PATH_NP)
            for folder_id in self.config.FOLDER_ID_P:
                self.download_pdfs_from_folder(folder_id, self.config.DOWNLOAD_PATH_P)
        except Exception as e:
            print(f"Error during the download process: {e}")
            raise e
