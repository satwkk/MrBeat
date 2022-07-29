from src.extract import SongExtractor, SpotifySongExtractor, YoutubeSongExtractor

''' 
Factory class that returns extractor instance based on some checks. 
'''
class ExtractorFactory:
    
    ''' 
    Returns an instance of SongExtractor based on url. 
    @param: url = The url or keyword provided by user.
    '''
    def get_extractor(self, url: str) -> SongExtractor:
        if url.__contains__("spotify.com"):
            return SpotifySongExtractor()
        
        return YoutubeSongExtractor()