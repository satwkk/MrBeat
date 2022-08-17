from urllib import request, parse

def parseUrl(url: str):
    res = parse.urlsplit(url)
    print(res)
    
    
parseUrl("https://open.spotify.com/playlist/2M6Y13hSQkCwodeOUieUom")