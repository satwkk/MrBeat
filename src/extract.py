from urllib import parse
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from src import utils
from src.youtube import Youtube, Song
from src.utils import get_id_from_url
from src.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

''' 
Base class for extracting songs. 
'''
class SongExtractor:
    player = Youtube()
    
    def __init__(self) -> None: ...

    '''
    Extracts audio information from given url or keyword.
    @param: url - The url of a specific track from spotify.
    '''
    def extract(self, url: str): ...

class YoutubeSongExtractor(SongExtractor):
    def __init__(self) -> None:
        super().__init__()
        
    def extract(self, keyword: str) -> Song:
        return self.player.extract_info(keyword)

class SpotifySongExtractor(SongExtractor):
    def __init__(self) -> None:
        super().__init__()
        self.streaming_uri = "open.spotify.com"
        self.auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        self.sp = Spotify(auth_manager=self.auth_manager)
    
    def get_meta_data(self, track) -> tuple[str, str]:
        if track is None: return
        name = track.get('name')
        artist = track.get('artists')[0] \
            .get('name') \
                .encode('ascii', 'ignore') \
                    .decode('latin-1')
        return (name, artist)
            
    def extract(self, url: str) -> Song:
        assert(parse.urlsplit(url).netloc == self.streaming_uri)
        track = self.sp.track(get_id_from_url(url))
        song, artist = self.get_meta_data(track)
        return self.player.extract_info(f"{song} - {artist}")

class SpotifyPlaylistExtractor(SpotifySongExtractor):
    def __init__(self) -> None:
        super().__init__()

    def extract(self, url: str) -> dict[str, str]:
        assert(parse.urlsplit(url).netloc == self.streaming_uri)
        urls = dict()
        tracks = self.sp.playlist_tracks(get_id_from_url(url))
        for item in tracks['items']:
            track = item.get('track')
            song, artist = self.get_meta_data(track)
            urls[song] = artist
        return urls

class SpotifyAlbumExtractor(SpotifySongExtractor):
    def __init__(self) -> None:
        super().__init__()

    def extract(self, url: str) -> dict[str, str]:
        assert(parse.urlsplit(url).netloc == self.streaming_uri)
        urls = dict()
        tracks = self.sp.album_tracks(get_id_from_url(url))
        for item in tracks['items']:
            song, artist = item['name'], ', '.join(artist['name'] for artist in item['artists'])
            urls[song] = artist
        return urls