from __future__ import annotations

import os

from bs4 import BeautifulSoup
from urllib import parse
from urllib.request import unquote

from vg_music_scraper.utils import request

class Song:
    def __init__(self, name: str, url: str, cd: str, correlative: str, download_url: str = None):
        self.name = name
        self.url = url
        self.cd = cd
        self.correlative = correlative
        self.download_url = download_url

    @property
    def file_name(self):
        if(self.download_url == None):
            raise Exception("The download url is required to get file name for the song")
        # download_url = 'https://dl.vgmdownloads.com/soundtracks/street-fighter-alpha-2-snes-gamerip-1996/szacsuhdda/01.%20Opening.mp3'
        url_parsed = parse.urlparse(self.download_url)
        # url_parsed.path = '/soundtracks/street-fighter-alpha-2-snes-gamerip-1996/szacsuhdda/01.%20Opening.mp3'
        default_name = unquote(os.path.basename(url_parsed.path))
        # default_name = '01. Opening.mp3'
        base_file_name, extension = os.path.splitext(default_name)
        # base_file_name = '01. Opening' // extension = '.mp3'
        return base_file_name.replace(' ', '_') + extension

    @classmethod
    def from_dictionary(cls, dictionary: dict[str, any]) -> Song:
        return cls(
            name=dictionary['name'],
            cd=dictionary['cd'],
            correlative=dictionary['correlative'],
            url=dictionary['url'],
            download_url=dictionary['download_url'],
        )
    
    def get_information(self: Song) -> None:
        response = request('get', self.url)
        content = response.content
        html = BeautifulSoup(content, 'html.parser')
        audio_player = html.find('audio', { 'id': 'audio' })
        source_url = audio_player.get('src')
        self.download_url = source_url
