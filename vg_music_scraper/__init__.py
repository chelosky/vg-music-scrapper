import multiprocessing
import os
import signal
import urllib3
from tqdm import tqdm
from urllib import parse
from urllib.request import unquote
from pathvalidate import sanitize_filename

from bs4 import BeautifulSoup
from vg_music_scraper.utils import request
from vg_music_scraper.cmdline import parse_args
from vg_music_scraper.album import Album
from vg_music_scraper.song import Song

semaphore = multiprocessing.Semaphore(1)
urllib3.disable_warnings()

def cli(): 
	album_urls = parse_args()

	for album_url in album_urls:
		album = Album.from_url(album_url=album_url)
		print('STARTING PROCESS FOR {title} ALBUM...'.format(title=album.title))
		print('GETTING INFORMATION ABOUTS SONGS...')
		album.songs = get_songs_information(album.songs)
		print('DOWNLOADING SONGS...')
		folder_name = sanitize_filename(album.title)
		download_songs(folder_name, album.songs)

def get_songs_information(songs: list[Song]):
	pool = multiprocessing.Pool(processes=5, initializer=init_worker)
	pbar = tqdm(total=len(songs))
	all_results = [
		pool.apply_async(
			get_song_information, 
			args=(song,),
			callback= lambda _ : pbar.update(1)
		)
		for song in songs
	]
	pool.close()
	pool.join()
	pbar.close()
	return [result.get() for result in all_results]

def download_songs(folder_name: str, songs: list[Song]):
	pool = multiprocessing.Pool(processes=5, initializer=init_worker)
	pbar = tqdm(total=len(songs))
	for song in songs:
		pool.apply_async(
			download_song, 
			args=(folder_name, song.download_url,),
			callback= lambda _ : pbar.update(1)
		)
	pool.close()
	pool.join()
	pbar.close()

def get_song_information(song: Song):
	response = request('get', song.url)
	content = response.content
	html = BeautifulSoup(content, 'html.parser')
	audio_player = html.find('audio', { 'id': 'audio' })
	source_url = audio_player.get('src')
	song.download_url = source_url
	return song

def download_song(folder_name: str, url: str):
	basePath = os.path.join('./audios', folder_name)
	os.makedirs(basePath, exist_ok=True)
	url_parsed = parse.urlparse(url)
	default_name = unquote(os.path.basename(url_parsed.path))
	base_file_name, extension = os.path.splitext(default_name)
	save_file_path = os.path.join(basePath, base_file_name.replace(' ', '_')) + extension
	response = request('get', url, stream=True)
	with open(save_file_path, "wb") as f:
		length = response.headers.get('content-length')
		if length is None:
			f.write(response.content)
		for chunk in response.iter_content(2048):
			f.write(chunk)

def init_worker():
    signal.signal(signal.SIGINT, subprocess_signal)

def subprocess_signal(sig, frame):
    if semaphore.acquire(timeout=1):
        print('Ctrl-C pressed, exiting sub processes ...')

    raise KeyboardInterrupt

if __name__ == "__main__": 
	cli()
