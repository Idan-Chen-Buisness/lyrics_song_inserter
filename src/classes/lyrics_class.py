import os

from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import re
import lyricsgenius as lg

from src.base import LoguruLogger, Config

LANGUAGE_NAMES = {
    'af': 'Afrikaans',
    'ar': 'Arabic',
    'bg': 'Bulgarian',
    'bn': 'Bengali',
    'ca': 'Catalan',
    'cs': 'Czech',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'es': 'Spanish',
    'et': 'Estonian',
    'fa': 'Persian',
    'fi': 'Finnish',
    'fr': 'French',
    'gu': 'Gujarati',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hr': 'Croatian',
    'hu': 'Hungarian',
    'id': 'Indonesian',
    'it': 'Italian',
    'ja': 'Japanese',
    'kn': 'Kannada',
    'ko': 'Korean',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'mk': 'Macedonian',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'ne': 'Nepali',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'pa': 'Punjabi',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'sq': 'Albanian',
    'sv': 'Swedish',
    'sw': 'Swahili',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tl': 'Tagalog',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
}
DetectorFactory.seed = 0


class Lyrics:
    def __init__(self):
        self.logger = LoguruLogger(__name__).get_logger()
        self.lyrics_config = Config().get_value('lyrics')
        self.api_key = os.getenv('GENIUS_API_KEY', self.lyrics_config['genius_api_key'])

    def is_lyrics_language_the_same_as_the_target(self, song_name, artist, target_language):
        lyrics = self.get_lyrics(song_name=song_name, artist_name=artist)
        if lyrics:
            song_language = self.detect_language(lyrics=lyrics)
            self.logger.debug(f"SONG: {song_name}, LYRICS: {song_language}, TARGET: {target_language} ")
            return target_language.lower() == song_language.lower()
        return False

    @staticmethod
    def detect_language(lyrics):
        try:
            language_code = detect(lyrics)
            language_name = LANGUAGE_NAMES.get(language_code, "Unknown language")
            return language_name
        except LangDetectException:
            return "Could not detect language"

    def get_lyrics(self, song_name, artist_name=None):

        query = song_name + " " + artist_name
        genius = lg.Genius(self.api_key, timeout=120, retries=5)
        search_results = genius.search_songs(query)

        if not search_results['hits']:
            self.logger.debug("No results found.")
            return None

        song = search_results['hits'][0]['result']
        for hit in search_results['hits']:
            if artist_name.lower().split(' ')[0] in hit['result']['artist_names'].lower():
                song = hit['result']
                try:
                    song_obj = genius.search_song(song_id=song['id'])
                    if song_obj:
                        break
                except Exception:
                    return None
        try:
            song_obj = genius.search_song(song_id=song['id'])
            song_lyrics = song_obj.lyrics
        except Exception as e:
            return None
        else:
            clean1 = "\n".join(song_lyrics.split('\n')[1:])
            cleaned_string = re.sub(r'\d+Embed', '', clean1)
            lyrics = re.sub(r'Embed$', '', cleaned_string)
            filtered_lyrics = [line for line in lyrics.split('\n') if not re.search(r'\[.*?\]', line)]
            cleaned_lyrics = '\n'.join(filtered_lyrics)
            self.logger.debug(f"Song name: {song_name} Lyrics retrieved successfully")
            return cleaned_lyrics
