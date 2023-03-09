from enum import Enum
from urllib import parse

from src.extractors import youtube, spotify

class ENetLoc(Enum):
    YOUTUBE=0
    SPOTIFY=1
    
# Maps the specified song url domain to respective Enum
def map_url_to_netloc(url: str) -> ENetLoc:
    netloc = parse.urlsplit(url).netloc 
    match netloc:
        case 'www.youtube.com':
            return ENetLoc.YOUTUBE
        case 'open.spotify.com':
            return ENetLoc.SPOTIFY

# Gets the path of the url (Ex: /playlist, /album)
# TODO: Implement a stack based algorithm
def get_path(url: str) -> str:
    path = parse.urlsplit(url).path
    return path.split('/')[1]

# Returns the callback functions based on path of url
path_table = {
    ENetLoc.YOUTUBE: {
        'watch': youtube.track_extract_yt
    },
    
    ENetLoc.SPOTIFY: {
        'track': spotify.track_extract_sp,
        'playlist': spotify.playlist_extract_sp,
        'album': spotify.album_extract_sp
    }
}
    
def extract(user_req: str):
    # If the keyword entered by user is a url
    if user_req.startswith('http'):
        netloc = map_url_to_netloc(user_req)
        return path_table[netloc][get_path(user_req)](user_req)
    
    # if the author has entered a keyword to perform a search
    return youtube.search_track(user_req)