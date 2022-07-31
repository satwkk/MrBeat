import re
import spotipy
import youtube_dl
import http.client
import concurrent.futures

from typing import List
from dataclasses import dataclass
from abc import ABC, abstractmethod
from src.config import BLACKLIST_CHARS
from spotipy.oauth2 import SpotifyClientCredentials
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

''' Base class for extracting songs. '''
class SongExtractor(ABC):
    @abstractmethod
    def extract_song(self, url: str): ...
    
    def sanitize_keyword(self, token: str) -> bool: 
        if token[0] in BLACKLIST_CHARS:
            return False
        return True

''' Child class of SongExtractor which extracts youtube audio from specified keyword. '''
class YoutubeSongExtractor(SongExtractor):
    def __init__(self) -> None:
        self.YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist':'True'}
        self.streaming_url = 'www.youtube.com'
        self.ytdl = youtube_dl.YoutubeDL(self.YDL_OPTIONS)
    
    # TODO: Use Youtube's API instead of regex.
    def extract_song(self, url: str) -> Song:
        if not self.sanitize_keyword(url): url = url[1:]
        conn = http.client.HTTPSConnection(self.streaming_url)
        conn.request('GET', f'/results?search_query={url.replace(" ", "+") if " " in url else url}')
        body = conn.getresponse().read()
        urls = re.findall(r'watch\?v=(\S{11})', body.decode())
        meta_data = self.ytdl.extract_info(urls[0], download=False)
        return Song(meta_data.get('url'), meta_data.get('title'), meta_data.get('thumbnail'))

''' Child class of SongExtractor which extracts youtube audio from spotify playlist url. '''
class SpotifySongExtractor(SongExtractor):
    def __init__(self) -> None:
        pass
        
    def extract_song(self, url: str):
        if "spotify.com" not in url: return
        
        extractor = YoutubeSongExtractor()
        urls = []
        
        auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        res = sp.playlist_tracks(url.split('/')[-2] if url.endswith('/') else url.split('/')[-1])
        songs = res["items"]
        for song in songs:
            urls.append(song["track"]["name"])
        return urls
        # return res["items"]
    
        # musics = res["items"]
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     for music in musics:
        #         future = executor.submit(extractor.extract_song, music['track']['name'])
        #         song = future.result()
        #         urls.append(song.url)
                
        # return urls   

