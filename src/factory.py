from src.extract import TrackExtractor, SpotifyPlaylistExtractor, SpotifyTrackExtractor, YoutubeTrackExtractorKeyword, SpotifyAlbumExtractor, YoutubeTrackExtractorURL
from urllib import parse

''' 
Factory class that returns extractor instance based on some checks. 
'''
class ExtractorFactory:
    
    ''' 
    Returns an instance of SongExtractor based on url. 
    @param: url = The url or keyword provided by user.
    '''
    def getExtractor(self, url: str) -> TrackExtractor:
        parsed_url = parse.urlsplit(url)
        netloc, path = parsed_url.netloc, parsed_url.path

        if netloc == 'open.spotify.com':
            if 'playlist' in path: return SpotifyPlaylistExtractor()
            elif 'album' in path: return SpotifyAlbumExtractor()
            return SpotifyTrackExtractor()

        elif netloc == 'www.youtube.com': return YoutubeTrackExtractorURL()

        # Default extractor for keyword based searches (DO NOT CHANGE THIS !)
        return YoutubeTrackExtractorKeyword()
    
    def get_yt_extractor_keyword(self) -> TrackExtractor:
        return YoutubeTrackExtractorKeyword()

    def get_yt_extractor_url(self) -> TrackExtractor:
        return YoutubeTrackExtractorURL()
    
    def get_sp_song_extractor(self) -> TrackExtractor:
        return SpotifyTrackExtractor()
    
    def get_sp_playlist_extractor(self) -> TrackExtractor:
        return SpotifyPlaylistExtractor()
