import sqlite3
from typing import List

from cprint import cprint

class PlayListManager():
    def __init__(self):
        self.conn = sqlite3.connect("test.db")
        self.cursor = self.conn.cursor()
    
    # TODO: Take the token as reference and change it's state without returning anything
    def sanitize_input(self, token: str):
        if token.__contains__(' '):
            return "".join([t for t in token.split(' ')])
        return token
        
    # TODO: We assume the table name does not contain space or vulnerable characters.
    def create_playlist(self, name: str):
        name = self.sanitize_input(name)
        self.cursor.execute(f'''create table if not exists {name} (song text)''')
        self.conn.commit()
        return name

    def insert_playlist(self, name: str, song: str):
        try:
            self.cursor.execute (f"insert into {name} values ('{song}')")
            self.conn.commit()
        except Exception as e:
            cprint.err(f"Could not insert song {song} into playlist")
            pass
        
    # DEBUG
    def get_playlist(self, table_name: str) -> List[str]:
        self.cursor.execute(f"select * from {self.sanitize_input(table_name)}")
        return self.cursor.fetchall()
    
    def list_tables(self):
        self.cursor.execute(f"select name from sqlite_master where type='table';")
        return self.cursor.fetchall()
        
    def cleanup(self):
        self.cursor.close()
        self.conn.close()