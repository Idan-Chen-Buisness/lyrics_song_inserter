import copy
import re
import pandas as pd
from datetime import datetime

from src.base import LoguruLogger, Config


class KworbClass:
    def __init__(self):
        self.kworb_config = Config().get_value('kworb')
        self.logger = LoguruLogger(__name__).get_logger()
        self.general_urls = self.kworb_config['general']
        self.youtube_urls = self.kworb_config['youtube_urls']

    def add_metadata_to_list_youtube(self, lst_of_songs):
        updated_lst_of_songs = []
        for song in lst_of_songs:
            new_song = copy.deepcopy(song)  # Create a new copy of the song dictionary
            new_song['is_published'] = False
            new_song['similarity_score'] = None
            new_song['type'] = "kworb"
            new_song['error'] = None
            new_song['date_created'] = datetime.now()
            updated_lst_of_songs.append(new_song)
        return updated_lst_of_songs

    def add_metadata_to_list_all_time_hits(self, lst_of_songs):
        updated_lst_of_songs = []
        for song in lst_of_songs:
            for lang in ['Hindi','Korean']:
            #for lang in ['Hindi','Portuguese','Korean', 'Spanish', 'Hebrew']:
                new_song = copy.deepcopy(song)  # Create a new copy of the song dictionary
                new_song['is_published'] = False
                new_song['similarity_score'] = None
                new_song['error'] = None

                new_song['date_created'] = datetime.now()
                new_song['target_language'] = lang
                updated_lst_of_songs.append(new_song)
        return updated_lst_of_songs

    def data_cleaning_youtube(self, df, column_name):
        df = df[~df[column_name].str.contains('short', case=False)]
        df = df[df[column_name].str.contains(' - ', case=False)]
        df = df[~df[column_name].apply(self.contains_arabic)]
        df['song_name'] = df[column_name].apply(lambda video: video.split(' - ')[1].strip())
        df['artist_names'] = df[column_name].apply(lambda video: video.split(' - ')[0].strip())
        df = df.rename(columns={'Wks': 'week'})
        df = df[['song_name', 'artist_names', 'week', 'target_language']]
        lst_of_songs = df.to_dict(orient="records")
        lst_of_songs = self.add_metadata_to_list_youtube(lst_of_songs=lst_of_songs)
        return lst_of_songs

    def data_cleaning_all_times_hits(self, df, column_name):
        df = df[~df[column_name].str.contains('short', case=False)]
        df = df[~df[column_name].apply(self.contains_arabic)]
        df[column_name] = df[column_name].apply(self.remove_after_official)
        df = df[df[column_name].str.contains(' - ', case=False)]
        df['song_name'] = df[column_name].apply(lambda video: video.split(' - ')[1].strip())
        df['song_name'] = df[column_name].apply(lambda video: video.split(' - ')[1].strip())
        df['artist_names'] = df[column_name].apply(lambda video: video.split(' - ')[0].strip())
        df = df[['song_name', 'artist_names']]
        lst_of_songs = df.to_dict(orient="records")
        lst_of_songs = self.add_metadata_to_list_all_time_hits(lst_of_songs=lst_of_songs)
        return lst_of_songs

    def fetch_songs(self):
        yield from self.extract_youtube()
        # yield from self.extract_general_url()

    def extract_general_url(self):
        # extract the html from the website and clean the data
        for url in self.general_urls:
            self.logger.info(f"Extracting from {url}")
            df = pd.read_html(url)[0]
            lst_of_songs = self.data_cleaning_all_times_hits(df=df, column_name='Video')
            yield lst_of_songs

    def extract_youtube(self):
        # extract the html from the website and clean the data
        for lang, url in self.youtube_urls.items():
            self.logger.info(f"Extracting from {url}")
            df = pd.read_html(url)[0]
            df['target_language'] = lang
            lst_of_songs = self.data_cleaning_youtube(df=df, column_name='Track')
            yield lst_of_songs

    @staticmethod
    def contains_arabic(text):
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
        return arabic_pattern.search(text) is not None

    @staticmethod
    def remove_after_official(text):
        lower_text = text.lower()
        keyword = 'official'
        keyword_index = lower_text.find(keyword)

        if keyword_index != -1:
            return text[:keyword_index - 1].strip()
        return text
