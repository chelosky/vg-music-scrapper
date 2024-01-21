import multiprocessing
import urllib3
import os
from tqdm import tqdm
from vg_music_scraper.config import config

from vg_music_scraper.song import Song
from vg_music_scraper.utils import download_file

urllib3.disable_warnings()
semaphore = multiprocessing.Semaphore(1)

class Downloader:
    @staticmethod
    def get_songs_download_information(songs: list[Song]) -> list[Song]:
        pbar = tqdm(total=len(songs))
        with multiprocessing.Pool(processes=config.DOWNLOADER_POOL_PROCESSES) as pool:
            all_results = [
                pool.apply_async(
                    Downloader._get_song_information, 
                    args=(song,),
                    callback= lambda _ : pbar.update(1)
                )
                for song in songs
            ]
            pool.close()
            pool.join()
            pbar.close()
        return [result.get() for result in all_results]
    
    @staticmethod
    def download_songs(folder_name: str, songs: list[Song]):
        pbar = tqdm(total=len(songs))
        with multiprocessing.Pool(processes=config.DOWNLOADER_POOL_PROCESSES) as pool:
            for song in songs:
                pool.apply_async(
                    Downloader._download_song, 
                    args=(song, folder_name),
                    callback= lambda _ : pbar.update(1)
                )
            pool.close()
            pool.join()
            pbar.close()

    def _download_song(song: Song, folder_name: str,): 
        basePath = os.path.join('./', config.FOLDER_DOWNLOADS, folder_name)
        os.makedirs(basePath, exist_ok=True)

        download_file(
            url=song.download_url,
            file_path=os.path.join(basePath, song.file_name) 
        )
        
    
    def _get_song_information(song: Song):
        song.get_information()
        return song
