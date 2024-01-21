import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from vg_music_scraper.constant import DEFAULT_DOWNLOADER_POOL_PROCESSES, DEFAULT_FOLDER_DOWNLOADS

load_dotenv()

class Config(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = os.getenv('DEBUG', False)
    FOLDER_DOWNLOADS: str = os.getenv('FOLDER_DOWNLOADS', DEFAULT_FOLDER_DOWNLOADS)
    DOWNLOADER_POOL_PROCESSES: int = os.getenv('DOWNLOADER_POOL_PROCESSES', DEFAULT_DOWNLOADER_POOL_PROCESSES)

config: Config = Config()