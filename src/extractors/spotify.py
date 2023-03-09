from typing import List
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from src.models.track import Track
from src.utils import get_id_from_url
from src.extractors.youtube import search_track
from src.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

AUTH_MANAGER = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp_client = Spotify(auth_manager=AUTH_MANAGER)

def track_extract_sp(url: str) -> Track:
    track = sp_client.track(get_id_from_url(url))
    if not track: return None
    song, artist = track['name'], \
        ', '.join(artist['name']
                    .encode('ascii', 'ignore')
                    .decode('latin-1') 
                    for artist in track['artists']
                    )
    return search_track(f'{song} - {artist}')
    
def playlist_extract_sp(url: str) -> List[Track]:
    playlist = list()
    tracks = sp_client.playlist_items(get_id_from_url(url))
    for item in tracks['items']:
        track = item['track']
        # TODO: This could cause some error
        if not track: return None
        song, artist = track['name'], \
                    ', '.join(artist['name']
                    .encode('ascii', 'ignore')
                    .decode('latin-1') 
                    for artist in track['artists']
                    )
        
        playlist.append(Track(artist, song))
    return playlist

def album_extract_sp(url: str) -> List[Track]:
    playlist = list()
    tracks = sp_client.album_tracks(get_id_from_url(url))
    for item in tracks['items']:
        song, artist = item['name'], ', '.join(artist['name'] for artist in item['artists'])
        playlist.append(Track(artist, song))
    return playlist
