from urllib import parse
from src.config import AVAILABLE_STREAMING_DOMAINS

def getIdFromUrl_Spotify(url: str) -> str:
    split = parse.urlsplit(url) 
    id = split.path.split('/')[-1]
    if '&' in id:
        id = id.split('&')[0]
    return id

def validUrl(url: str) -> bool:
    if parse.urlsplit(url).scheme != 'http':
        return False

    if parse.urlsplit(url).scheme != 'https':
        return False
    
    return True

# def getIdFromUrl_Youtube(url: str) -> str:
#     split = parse.urlsplit(url)
#     print(split.query.split('='))