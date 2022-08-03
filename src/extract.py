import re
import spotipy
import youtube_dl
import http.client

from typing import List
from cprint import cprint
from dataclasses import dataclass
from abc import ABC, abstractmethod
from src.config import BLACKLIST_CHARS
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_dl.utils import ExtractorError, DownloadError
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
        self.YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist':'True'}
        self.streaming_url = 'www.youtube.com'
        self.ytdl = youtube_dl.YoutubeDL(self.YDL_OPTIONS)
        
    def _extract_song(self, url, download=False):
        try:
            return self.ytdl.extract_info(url, download=download)
        except ExtractorError as extractError:
            cprint.err("Cannot extract audio stream. Maybe paid video ??? ")
        except DownloadError as downloadError:
            cprint.err(f"Cannot download audio stream from video.")
        
    def extract_song(self, url: str) -> Song:
        if not self.sanitize_keyword(url): url = url[1:]
        conn = http.client.HTTPSConnection(self.streaming_url)
        conn.request('GET', f'/results?search_query={url.replace(" ", "+") if " " in url else url}')
        body = conn.getresponse().read()
        urls = re.findall(r'watch\?v=(\S{11})', body.decode())
        meta_data = self._extract_song(urls[0])
        return Song(meta_data.get('url'), meta_data.get('title'), meta_data.get('thumbnail'))

''' 
Child class of SongExtractor which extracts youtube audio from spotify playlist url. 
'''
class SpotifySongExtractor(SongExtractor):
    def __init__(self) -> None:
        pass
    
    def extract_song(self, url: str):
        if "spotify.com" not in url: return
        
        urls = dict()
        
        auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        res = sp.playlist_tracks(url.split('/')[-2] if url.endswith('/') else url.split('/')[-1])
        
        items = res["items"]
        
        for item in items:
            track = item.get('track')
            if track is not None:
                song, artist  = track.get('name'), track.get('artists')[0].get('name').encode('ascii', 'ignore').decode('latin-1')
                urls[song] = artist
                
        return urls
