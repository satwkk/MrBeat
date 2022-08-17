import spotipy

from urllib import parse
from abc import ABC, abstractmethod
from spotipy.oauth2 import SpotifyClientCredentials

from src.player import YoutubePlayer, Song
from src.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
        
''' 
Base class for extracting songs. 
'''
class SongExtractor(ABC):
    @abstractmethod
    def extract_song(self, url: str): ...

''' 
Child class of SongExtractor which extracts youtube audio from specified keyword. 
'''
class YoutubeSongExtractor(SongExtractor):
    def __init__(self) -> None:
        self.player = YoutubePlayer()

    def extract_song(self, keyword: str) -> Song:
        return self.player.extract_info(keyword)
    
''' 
Child class of SongExtractor which extracts youtube audio from spotify playlist url. 
'''
class SpotifySongExtractor(SongExtractor):
    def __init__(self) -> None:
        ...
        
    def extract_song(self, url: str):
        urls = dict()
        res = parse.urlsplit(url)
        
        if res.netloc != "open.spotify.com": return
        auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        res = sp.playlist_tracks(url.split('/')[-2] if url.endswith('/') else url.split('/')[-1])
        
        for item in res["items"]:
            track = item.get('track')
            if track is not None:
                song = track.get('name')
                artist = track.get('artists')[0].get('name').encode('ascii', 'ignore').decode('latin-1')
                urls[song] = artist
                
        return urls
