import os
from dotenv import load_dotenv

load_dotenv()

COMMAND_PREFIX = '-'
YT_SEARCH_FMT = '{} - {}'
BLACKLIST_CHARS = ["#", "?", "&", "="]
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
AVAILABLE_STREAMING_DOMAINS = ["www.youtube.com", "youtube.com", "open.spotify.com"]
INVOKER_NOT_JOINED_ALERT = "Join a voice channel before invoking music commands."
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}