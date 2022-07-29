import pathlib

class FileWriter():
    def __init__(self, path: str, filename: str, encoding: str) -> None:
        self.path = path
        self.filename = filename
        self.encoding = encoding
        self.handle = pathlib.Path(self.path)
    
    # TODO: Check if the directory exists or not, if not create the directory.
    def write(self, contents: str):
        log_dir = self.handle / "logs"
        with (log_dir / self.filename).open("a", encoding=self.encoding) as log_file:
            log_file.write(contents)