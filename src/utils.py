from urllib import parse

def get_id_from_url(url: str) -> str:
    split = parse.urlsplit(url) 
    id = split.path.split('/')[-1]
    if '&' in id: id = id.split('&')[0]
    return id
