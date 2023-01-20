import os
from dotenv import load_dotenv

load_dotenv()

BLACKLIST_CHARS = ["#", "?", "&", "="]
SQL_BLACKLIST_CHARS = ["'", " "]
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
AVAILABLE_STREAMING_DOMAINS = ["www.youtube.com", "youtube.com", "open.spotify.com"]
INVOKER_NOT_JOINED_ALERT = "Stop disturbing others dumbo, join a voice channel if you want to listen music."
