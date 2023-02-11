from src.extract import SongExtractor, SpotifyPlaylistExtractor, SpotifySongExtractor, YoutubeSongExtractor, SpotifyAlbumExtractor

''' 
Factory class that returns extractor instance based on some checks. 
'''
class ExtractorFactory:
    
    ''' 
    Returns an instance of SongExtractor based on url. 
    @param: url = The url or keyword provided by user.
    '''
    def getExtractor(self, url: str) -> SongExtractor:
        if url.__contains__("open.spotify.com"):
            if "playlist" in url:
                return SpotifyPlaylistExtractor()
            elif 'album' in url:
                return SpotifyAlbumExtractor()
            
            return SpotifySongExtractor()
        
        return YoutubeSongExtractor()
    
    def getYoutubeSongExtractor(self) -> SongExtractor:
        return YoutubeSongExtractor()
    
    def getSpotifySongExtractor(self) -> SongExtractor:
        return SpotifySongExtractor()
    
    def getSpotifyPlaylistExtractor(self) -> SongExtractor:
        return SpotifyPlaylistExtractor()