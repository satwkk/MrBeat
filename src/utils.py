from urllib import parse

'''
Gets the ID from a spotify URL by parsing the URL.
'''
def getIdFromUrl_Spotify(url: str) -> str:
    split = parse.urlsplit(url) 
    id = split.path.split('/')[-1]
    if '&' in id:
        id = id.split('&')[0]
    return id

'''
Gets the ID from a youtube URL by parsing the URL.
'''
# https://www.youtube.com/playlist ? list=PLeo1K3hjS3uu_n_a__MI_KktGTLYopZ12
# https://www.youtube.com/watch ? v=jJqeaj2VuQA

def getIdFromUrl_Youtube(url: str) -> str:
    split = parse.urlsplit(url)
    print(split.query.split('='))