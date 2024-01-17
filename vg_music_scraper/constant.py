# coding: utf-8
import os

DEBUG = os.getenv('DEBUG', False)
BASE_URL = 'https://downloads.khinsider.com'
FOLDER_DOWNLOADS = os.getenv('FOLDER_DOWNLOADS', 'albums')