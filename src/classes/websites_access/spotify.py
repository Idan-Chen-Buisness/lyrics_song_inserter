import copy
import re
import pandas as pd
from datetime import datetime

import requests

from src.base import LoguruLogger, Config


class Spotify:
    def __init__(self):
        self.config = Config().get_value('spotify')
        self.logger = LoguruLogger(__name__).get_logger()

        self.playlists_id = self.config['playlists_id']
        self.client_id = self.config['auth']['client_id']
        self.client_secret = self.config['auth']['client_secret']
        self.access_token = self.get_access_token()

    def get_access_token(self):
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })
        auth_response_data = auth_response.json()
        access_token = auth_response_data['access_token']
        return access_token

    def get_top_tracks(self, lang, playlist_id):
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        response = requests.get(url, headers={
            'Authorization': f'Bearer {self.access_token}'
        })
        data = response.json()
        tracks = []
        for index, item in enumerate(data['items']):
            track = item['track']
            tracks.append({
                'is_published': False,
                'week': index+1,
                'type': "spotify",
                'similarity_score': None,
                'error': None,
                'date_created': datetime.now(),
                'target_language': lang,
                'song_name': track['name'],
                'artist_names': track['artists'][0]['name'],
            })
        return tracks

    def extract_tracks_from_playlists(self):
        for lang, playlist_id in self.playlists_id.items():
            a = self.get_top_tracks(lang=lang,
                                    playlist_id=playlist_id)
            yield a

    def fetch_songs(self):
        yield from self.extract_tracks_from_playlists()
