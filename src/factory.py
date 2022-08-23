from src.extract import SongExtractor, SpotifyPlaylistExtractor, SpotifySongExtractor, YoutubeSongExtractor

''' 
Factory class that returns extractor instance based on some checks. 
'''
class ExtractorFactory:
    
    ''' 
    Returns an instance of SongExtractor based on url. 
    @param: url = The url or keyword provided by user.
    '''
    def getExtractor(self, url: str) -> SongExtractor:
        if url.__contains__("spotify.com"):
            if url.__contains__("playlist"):
                return SpotifyPlaylistExtractor()
            
            return SpotifySongExtractor()
        
        return YoutubeSongExtractor()
    
    def getYoutubeSongExtractor(self) -> SongExtractor:
        return YoutubeSongExtractor()
    
    def getSpotifySongExtractor(self) -> SongExtractor:
        return SpotifySongExtractor()
    
    def getSpotifyPlaylistExtractor(self) -> SongExtractor:
        return SpotifyPlaylistExtractor()