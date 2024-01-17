import argparse

def parse_args() -> list[str]:
    parser = argparse.ArgumentParser("Welcome to VG Music Scraper")
    parser.add_argument(
        "-a",
        "--album",
        help="Pass in a album url inline",
        nargs="+",
        action="append",
    )

    args = parser.parse_args()

    albums = sum(args.album or [[]], [])

    if len(albums) == 0:
        while True:
            name = input("Enter albums url (leave blank to stop): ").strip()
            if name == "":
                break
            albums.append(name)

    return albums