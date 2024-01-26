import argparse

def parse_args() -> (list[str], bool, bool):
    parser = argparse.ArgumentParser("Welcome to VG Music Scraper")
    parser.add_argument(
        "-a",
        "--album",
        dest='albums',
        action="append",
        nargs="+",
        default=[],
        help="Pass in a album url inline",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        dest='force_fetch',
        default=False,
        help="Force fetch of album information and omit cache files",
    )
    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        dest='download_songs',
        default=False,
        help="Download the album songs into the downloads folder",
    )

    options = parser.parse_args()

    album_urls = sum(options.albums or [[]], [])
    force_fetch: bool = options.force_fetch
    download_songs: bool = options.download_songs

    if len(album_urls) == 0:
        while True:
            name = input("Enter album url (leave blank to stop): ").strip()
            if name == "":
                break
            album_urls.append(name)

    return album_urls, force_fetch, download_songs