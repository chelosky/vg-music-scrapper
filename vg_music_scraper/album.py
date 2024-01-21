from __future__ import annotations

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from vg_music_scraper.song import Song
from vg_music_scraper.utils import request
from vg_music_scraper.constant import BASE_URL

class Album:
    def __init__(self, 
                 id: str,
                 title: str, 
                 alternative_title: str = None,
                 songs: list[Song] = []
                 ):
        self.id = id
        self.title = title
        self.alternative_title = alternative_title
        self.songs = songs
 
    @property
    def folder_name(self) -> str:
        return sanitize_filename(self.title)

    @classmethod
    def from_url(cls, album_url: str) -> Album:
        response = request('get', album_url)
        content = response.content

        html = BeautifulSoup(content, 'html.parser')
        page_content = html.find('div', { 'id': 'pageContent' })

        '''Album general information'''
        album_id = page_content.find('div', { 'class': 'albumMassDownload' }).select_one('a').get('href').split('/')[-1]
        title = page_content.select_one('h2').text;
        alternative_title = page_content.find('p', { 'class': 'albuminfoAlternativeTitles' })
        alternative_title = None if alternative_title is None else alternative_title.text 

        '''TODO: IMPLEMENT LOGIC TO PARSE THE ALBUM INFO'''
        metaData = page_content.find('p', { 'align': 'left' })

        '''Songs information'''
        song_table = page_content.find('table', { 'id': 'songlist' })
        header_row_content = song_table.find('tr', { 'id': 'songlist_header' }).text;
        
        TABLE_HEADER_FLAGS = {
            'CD': 'CD' in header_row_content,
            'CORRELATIVE': '#' in header_row_content,
            'TITLE': 'Song Name' in header_row_content
        }

        TABLE_HEADERS_POSITION = {
            'CD': 2,
            'CORRELATIVE': 2 + int(TABLE_HEADER_FLAGS['CD']),
            'TITLE': 2 + int(TABLE_HEADER_FLAGS['CD']) + int(TABLE_HEADER_FLAGS['CORRELATIVE'])
        }

        songs_list = [
            Song.from_dictionary(
                { 
                    'cd': int(song.select_one(':nth-child({position})'.format(position=TABLE_HEADERS_POSITION['CD'])).text.replace('.','')) 
                            if TABLE_HEADER_FLAGS['CD'] 
                            else None, 
                    'correlative': int(song.select_one(':nth-child({position})'.format(position=TABLE_HEADERS_POSITION['CORRELATIVE'])).text.replace('.','')) 
                            if TABLE_HEADER_FLAGS['CORRELATIVE'] 
                            else None, 
                    'name': sanitize_filename(song.select_one(':nth-child({position})'.format(position=TABLE_HEADERS_POSITION['TITLE'])).text), 
                    'url': "{base_url}{song_url}".format(
                        base_url=BASE_URL, 
                        song_url=song.select_one(':nth-child({position})'.format(position=TABLE_HEADERS_POSITION['TITLE']))
                                    .select_one('a')
                                    .get('href')
                    ),
                    'download_url': None
                }
            )
            for song in song_table.find_all('tr') 
            if not song.get('id') in ['songlist_header', 'songlist_footer']
        ]

        return cls(
            id=album_id,
            title=title,
            alternative_title = alternative_title,
            songs = songs_list
        )
