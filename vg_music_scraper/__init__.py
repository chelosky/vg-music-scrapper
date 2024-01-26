import os
from vg_music_scraper.constant import ALBUM_DATA_FILE, DEFAULT_DOWNLOADER_POOL_PROCESSES, DEFAULT_FOLDER_DOWNLOADS
from vg_music_scraper.downloader import Downloader

from vg_music_scraper.cmdline import parse_args
from vg_music_scraper.album import Album
from vg_music_scraper.utils import create_json_file, read_json_file

def cli(): 
	(album_urls, force_fetch, download_songs) = parse_args()

	for album_url in album_urls:
		fetch_album(album_url=album_url, force_fetch=force_fetch, download_songs=download_songs)
	

def fetch_album(album_url: str, force_fetch: bool = True, download_songs: bool = False) -> Album:
	album = Album.from_url(album_url=album_url)
	print('STARTING PROCESS FOR {title} ALBUM...'.format(title=album.title))

	album_file_path = os.path.join(DEFAULT_FOLDER_DOWNLOADS, album.folder_name,ALBUM_DATA_FILE)
	cache_file = read_json_file(file_path=album_file_path)

	downloader = Downloader(poll_process_nbr=DEFAULT_DOWNLOADER_POOL_PROCESSES, download_folder_path=DEFAULT_FOLDER_DOWNLOADS)

	if(cache_file != None and not force_fetch):
		album = Album.from_dictionary(dict=cache_file)
	else:
		print('GETTING INFORMATION ABOUTS SONGS...')
		album.songs = downloader.get_songs_download_information(
			songs=album.songs
		)
		print('GENERATING DATA FILE JSON...')
		create_json_file(file_path=album_file_path, data=album.to_dict())
	
	if(download_songs):
		print('DOWNLOADING SONGS...')
		downloader.download_songs(folder_name=album.folder_name, songs=album.songs)

	print('PROCESS COMPLETED FOR {title} ALBUM!'.format(title=album.title))

	return album

if __name__ == "__main__": 
	cli()
