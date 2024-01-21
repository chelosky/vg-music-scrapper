from vg_music_scraper.downloader import Downloader

from vg_music_scraper.cmdline import parse_args
from vg_music_scraper.album import Album

def cli(): 
	album_urls = parse_args()

	for album_url in album_urls:
		album = Album.from_url(album_url=album_url)
		print('STARTING PROCESS FOR {title} ALBUM...'.format(title=album.title))
		print('GETTING INFORMATION ABOUTS SONGS...')
		album.songs = Downloader.get_songs_download_information(
			songs=album.songs
		)
		print('DOWNLOADING SONGS...')
		Downloader.download_songs(folder_name=album.folder_name, songs=album.songs)
		print('PROCESS COMPLETED FOR {title} ALBUM!'.format(title=album.title))
	print('PROCESS COMPLETED!')

if __name__ == "__main__": 
	cli()
