import spotipy

from typing import List
from pytube import Search
from dataclasses import dataclass
from abc import ABC, abstractmethod
from spotipy.oauth2 import SpotifyClientCredentials

from src.config import BLACKLIST_CHARS
from src.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

''' Song Data class to store information about song '''
@dataclass
class Song():
    url = None
    title = None
    thumbnail = None
    
    def __init__(self, url, title, thumbnail):
        self.url = url
        self.title = title
        self.thumbnail = thumbnail

''' 
Base class for extracting songs. 
'''
class SongExtractor(ABC):
    @abstractmethod
    def extract_song(self, url: str): ...

    def sanitize_keyword(self, token: str) -> bool: 
        if token[0] in BLACKLIST_CHARS:
            return False
        return True

''' 
Child class of SongExtractor which extracts youtube audio from specified keyword. 
'''
class YoutubeSongExtractor(SongExtractor):
    def __init__(self) -> None:
        ...

    def extract_song(self, url: str) -> Song:
        searchObj = Search(url)
        result = searchObj.results[0]
        audio_stream = result.streams.get_audio_only()
        return Song(audio_stream.url, result.title, result.thumbnail_url)

''' 
Child class of SongExtractor which extracts youtube audio from spotify playlist url. 
'''
class SpotifySongExtractor(SongExtractor):
    def __init__(self) -> None:
        ...
        
    def parseUrl(self):
        from urllib import parse
        parse.url
        
    def extract_song(self, url: str):
        if "spotify.com" not in url: return
        
        urls = dict()
        
        auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # TODO: Handle URL parsing with parameters in url
        res = sp.playlist_tracks(url.split('/')[-2] if url.endswith('/') else url.split('/')[-1])
        
        items = res["items"]
        
        for item in items:
            track = item.get('track')
            if track is not None:
                song = track.get('name')
                artist = track.get('artists')[0].get('name').encode('ascii', 'ignore').decode('latin-1')
                urls[song] = artist
                
        return urls
