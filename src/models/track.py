from dataclasses import dataclass

@dataclass
class Track:
    author_name: str
    track_title: str
    thumbnail_url: str = None
    audio_stream_url: str = None
    
    @property
    def playable(self):
        if not self.audio_stream_url: return False
        return True

