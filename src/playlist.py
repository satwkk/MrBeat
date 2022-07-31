import sqlite3
from typing import List

from cprint import cprint
from src.config import SQL_BLACKLIST_CHARS

class PlayListManager():
    def __init__(self):
        self.conn = sqlite3.connect("test.db")
        self.cursor = self.conn.cursor()
    
    def sanitize_input(self, token: str):
        for char in SQL_BLACKLIST_CHARS:
            if char in token:
                token = token.replace(char, "")
                return token
        return token
    
    # TODO: We assume the table name does not contain vulnerable characters.
    def create_playlist(self, name: str):
        name = self.sanitize_input(name)
        self.cursor.execute(f'''create table if not exists {name} (song text)''')
        self.conn.commit()
        return name

    def insert_playlist(self, name: str, song: str):
        try:
            song = self.sanitize_input(song)
            self.cursor.execute (f"insert into {name} values ('{song}')")
            self.conn.commit()
        except Exception as e:
            cprint.err(f"Could not insert song {song} into playlist")
            pass
    
    def list_tables(self):
        self.cursor.execute(f"select name from sqlite_master where type='table';")
        return self.cursor.fetchall()
    
    def get_contents(self, table: str):
        try:
            self.cursor.execute(f"select * from {table}")
            return self.cursor.fetchall()
        except Exception as e:
            cprint.err(f"Could not found table {table}.")
            return
        
    def cleanup(self):
        self.cursor.close()
        self.conn.close()