from pytube import Search
from youtube_dl import YoutubeDL

class Song:
    def __init__(self, **kwargs):
        self.__streamURL = kwargs.get('url')
        self.__title = kwargs.get('title')
        self.__description = kwargs.get('description')
        self.__author = kwargs.get('author')
        self.__thumbnail = kwargs.get('thumbnail')
        
    @property
    def audioStream(self):
        if self.__streamURL:
            return self.__streamURL
        
    @property
    def title(self):
        if self.__title:
            return self.__title
    
    @property
    def description(self):
        if self.__description:
            return self.__description
        
    @property
    def author(self):
        if self.__author:
            return self.__author
        
    @property
    def thumbnail(self):
        if self.__thumbnail:
            return self.__thumbnail

class Youtube(YoutubeDL):
    def __init__(self, params=None, auto_init=True):
        super().__init__({'format': 'bestaudio/best', 'noplaylist':'True', 'quiet': 'True', 'ignoreerrors': 'True'}, auto_init)
        self.__videoURI = 'https://www.youtube.com/watch?v={}'
        self.__keyword = None
    
    def extract_info(self, keyword: str, download: bool = False) -> Song:
        self.__keyword = keyword
        
        searchObj = Search(self.__keyword)
        metaData = super().extract_info(
            url=self.__videoURI.format(searchObj.results[0].video_id),
            download=download
        )
        
        return Song(
            url=metaData.get('url'), 
            title=metaData.get('title'), 
            author=metaData.get('author'), 
            description=metaData.get('description'),
            thumbnail=metaData.get('thumbnail')
        )