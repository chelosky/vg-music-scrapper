import os
import urllib3
from tqdm import tqdm
import multiprocessing

from vg_music_scraper.song import Song
from vg_music_scraper.utils import create_folder, download_file

urllib3.disable_warnings()
semaphore = multiprocessing.Semaphore(1)

class Downloader:
    def __init__(self, poll_process_nbr: int, download_folder_path: str):
        self.poll_process_nbr = poll_process_nbr
        self.download_folder_path = download_folder_path

    def get_songs_download_information(self, songs: list[Song]) -> list[Song]:
        pbar = tqdm(total=len(songs))
        with multiprocessing.Pool(processes=self.poll_process_nbr) as pool:
            all_results = [
                pool.apply_async(
                    self._get_song_information, 
                    args=(song,),
                    callback= lambda _ : pbar.update(1)
                )
                for song in songs
            ]
            pool.close()
            pool.join()
            pbar.close()
        return [result.get() for result in all_results]
    
    def download_songs(self, folder_name: str, songs: list[Song]):
        pbar = tqdm(total=len(songs))
        with multiprocessing.Pool(processes=self.poll_process_nbr) as pool:
            for song in songs:
                pool.apply_async(
                    self._download_song, 
                    args=(song, folder_name),
                    callback= lambda _ : pbar.update(1)
                )
            pool.close()
            pool.join()
            pbar.close()

    def _download_song(self, song: Song, folder_name: str,): 
        folder_path = os.path.join(self.download_folder_path, folder_name)
        create_folder(folder_path=folder_path)

        download_file(
            url=song.download_url,
            file_path=os.path.join(folder_path, song.file_name) 
        )
    
    def _get_song_information(self, song: Song):
        song.get_information()
        return song
    
