from urllib import parse

def getIdFromUrl_Spotify(url: str) -> str:
    split = parse.urlsplit(url) 
    id = split.path.split('/')[-1]
    if '&' in id:
        id = id.split('&')[0]
    return id

def validate_url(url: str, valid_netloc: str) -> bool:
    if parse.urlsplit(url).netloc == valid_netloc:
            return True
    return False