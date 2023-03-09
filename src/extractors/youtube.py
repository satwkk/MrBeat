from typing import List
from youtube_dl import YoutubeDL
from pytube import YouTube, Search

from src.models.track import Track

YOUTUBEDL_PARAMS = {'format': 'bestaudio/best', 'noplaylist':'True', 'quiet': 'True', 'ignoreerrors': 'True'}
ytdl_player = YoutubeDL(params=YOUTUBEDL_PARAMS, auto_init=True)

# Seaches the youtube for specified keyword and returns the first result
def search_track(keyword: str) -> Track:
    search_results = Search(keyword)
    meta_data = ytdl_player.extract_info('https://www.youtube.com/watch?v={}'.format(search_results.results[0].video_id), download=False)
    return Track(
        meta_data.get('author'),
        meta_data.get('title'),
        meta_data.get('thumbnail'),
        meta_data.get('url')
    )
    
def track_extract_yt(url: str) -> Track:
    search_results = YouTube(url)
    meta_data = ytdl_player.extract_info(url='https://www.youtube.com/watch?v={}'.format(search_results.video_id), download=False)
    return Track(
        meta_data.get('author'),
        meta_data.get('title'),
        meta_data.get('thumbnail'),
        meta_data.get('url')
    )
    
# TODO: Implement youtube playlist extractor
def playlist_extract_yt(url: str) -> List[Track]: ...
