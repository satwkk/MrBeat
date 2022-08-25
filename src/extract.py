from urllib import parse
from spotipy import Spotify
from typing import Optional
from spotipy.oauth2 import SpotifyClientCredentials

from src.youtube import Youtube, Song
from src.utils import getIdFromUrl_Spotify
from src.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
        
''' 
Base class for extracting songs. 
'''
class SongExtractor:
    player = Youtube()
    
    def __init__(self) -> None: ...
    def extractSong(self, url: str): ...

''' 
Child class of SongExtractor which extracts youtube audio from specified keyword. 
'''
class YoutubeSongExtractor(SongExtractor):
    def __init__(self) -> None:
        super().__init__()
        
    def extractSong(self, keyword: str) -> Song:
        return self.player.extract_info(keyword)

''' 
Child class of SongExtractor which extracts audio stream from youtube from spotify track URL.
'''
class SpotifySongExtractor(SongExtractor):
    def __init__(self) -> None:
        super().__init__()
        self.streamingURI = "open.spotify.com"
        self.auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        self.sp = Spotify(auth_manager=self.auth_manager)
        
    '''
    Checks if the domain is correct.
    @param: url - The domain from which to fetch details about the song. Which is spotify.com in this case.
    '''
    def validateNetLoc(self, url: str) -> bool:
        if parse.urlsplit(url).netloc != self.streamingURI:
            return False
        return True
    
    '''
    Gets the track's name and author's name.
    @param: track - It is a dictionary containing metadata about the track.
    # TODO: Some ascii letters in a song name seems to return NoneType causing the bot to error out.
    '''
    def getTrackDetails(self, track) -> tuple[str, str]:
        if track is None:
            return
        name = track.get('name')
        artist = track.get('artists')[0].get('name').encode('ascii', 'ignore').decode('latin-1')
        return (name, artist)
            
            
    '''
    Extracts meta data of a single audio from the given url.
    @param: url - The url of a specific track from spotify.
    '''
    def extractSong(self, url: str) -> Song:
        if not self.validateNetLoc(url): return
        track = self.sp.track(getIdFromUrl_Spotify(url))
        song, artist = self.getTrackDetails(track)
        return self.player.extract_info(f"{song} - {artist}")

'''
Child class fof SpotifySongExtractor which extracts audio streams from multiple youtube videos from spotify playlist URL.
'''
class SpotifyPlaylistExtractor(SpotifySongExtractor):
    def __init__(self) -> None:
        super().__init__()
    
    '''
    Extracts meta data of a single audio from the given url.
    @param: url - The url of a specific playlist from spotify.
    ''' 
    def extractSong(self, url: str):
        urls = dict()
        if not self.validateNetLoc(url): return
        tracks = self.sp.playlist_tracks(getIdFromUrl_Spotify(url))
        for item in tracks["items"]:
            track = item.get('track')
            song, artist = self.getTrackDetails(track)
            urls[song] = artist
        return urls
