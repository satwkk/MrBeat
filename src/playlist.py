import sqlite3
from typing import List

from cprint import cprint
from src.config import SQL_BLACKLIST_CHARS

'''
Playlist manager to manage adding and removing of playlists from the database.
'''
class PlayListManager():
    def __init__(self):
        self.conn = sqlite3.connect("test.db")
        self.cursor = self.conn.cursor()
    
    '''
    Searches for any SQL vulnerable characters in the query and replaces it with empty character
    @param: token - Name of table (playlist) passed by user.
    '''
    def sanitizeInput(self, token: str):
        for char in SQL_BLACKLIST_CHARS:
            if char in token:
                token = token.replace(char, "")
                return token
        return token
    
    '''
    Creates a playlist based on user input after performing some sanitization.
    @param: name - Name of the table (playlist) passed by user.
    '''
    def createPlaylist(self, name: str):
        try:
            name = self.sanitizeInput(name)
            self.cursor.execute(f'''create table if not exists {name} (song text)''')
            self.conn.commit()
            return name
        except Exception as e:
            cprint.err(f"Blacklisted chars in playlist name. Could not create table {name}")

    '''
    Inserts a song into the playlist.
    @param: name - Name of the  playlist.
    @param: song - The song keyword to add to the playlist.
    '''
    def insertPlaylist(self, name: str, song: str):
        try:
            song = self.sanitizeInput(song)
            self.cursor.execute (f"insert into {name} values ('{song}')")
            self.conn.commit()
        except Exception as e:
            cprint.err(f"Could not insert song {song} into playlist")
            pass
    
    '''
    Lists all tables (playlists) in the database.
    @param: None
    '''
    def listPlaylists(self):
        self.cursor.execute(f"select name from sqlite_master where type='table';")
        return self.cursor.fetchall()
    
    '''
    Gets all the songs from a certain playlist.
    @param: table - Name of the playlist
    '''
    def getContents(self, table: str):
        try:
            table = self.sanitizeInput(table)
            self.cursor.execute(f"select * from {table}")
            return self.cursor.fetchall()
        except Exception as e:
            cprint.err(f"Could not found table {table}.")
            

    '''
    Checks if the playlist to be created already exists in the database.
    @param: playlist - Name of the playlist to be created
    '''
    def bAlreadyExists(self, playlist: str) -> bool:
        tables = self.listPlaylists()
        for table in tables:
            if playlist == table[0]:
                return True
        return False

    def cleanup(self):
        self.cursor.close()
        self.conn.close()
