from src.classes import Manager


def main():
    manager = Manager()
    manager.fetch_song_and_insert_to_db()


if __name__ == '__main__':
    main()
