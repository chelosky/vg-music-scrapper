from __future__ import annotations

class Song:
    def __init__(self, name: str, url: str, cd: str, correlative: str, download_url: str = None):
        self.name = name
        self.url = url
        self.cd = cd
        self.correlative = correlative
        self.download_url = download_url

    @classmethod
    def from_dictionary(cls, dictionary: dict[str, any]) -> Song:
        return cls(
            name=dictionary['name'],
            cd=dictionary['cd'],
            correlative=dictionary['correlative'],
            url=dictionary['url'],
            download_url=dictionary['download_url'],
        )