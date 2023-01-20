import os
from dotenv import load_dotenv

load_dotenv()

COMMAND_PREFIX = '-'
BLACKLIST_CHARS = ["#", "?", "&", "="]
SQL_BLACKLIST_CHARS = ["'", " "]
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
AVAILABLE_STREAMING_DOMAINS = ["www.youtube.com", "youtube.com", "open.spotify.com"]
INVOKER_NOT_JOINED_ALERT = "Stop disturbing others dumbo, join a voice channel if you want to listen music."
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
