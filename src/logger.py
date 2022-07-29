import time
import discord

from src.handle import FileWriter
from cprint import cprint

# ================================================================================
# Base message class which inherits from discord's Message class
# ================================================================================

class BaseLogMessage():
    def __init__(self, message: discord.Message) -> None:
        self.pattern = f"[{time.ctime()}] " + "[{}] : [{}] {} sent => {}\n" # Log level, guild, author, message
        self.message = message
    
    # virtual function to be overriden by child classes
    def get_message(self):
        raise NotImplementedError("Must be overriden by child class")
    
    # prints the message to stdout
    def print_message(self):
        if isinstance(self, DebugLogMessage):
            cprint.info(self.get_message())
        elif isinstance(self, ErrorLogMessage):
            cprint.err(self.get_message())
        
    # returns name of the discord channel
    def get_guild_name(self):
        return self.message.guild.name

    # returns the name of the author who invoked the command
    def get_message_author(self):
        return self.message.author.display_name

    # returns the content of the message
    def get_message_content(self):
        return self.message.content
    
# ================================================================================
# Debug message class which inherits from Base message class.
# ================================================================================

class DebugLogMessage(BaseLogMessage):
    def __init__(self, message: discord.Message) -> None:
        super().__init__(message)

    # Formats the logging pattern.
    # RETURN: str => Returns the formated string for logging.
    def get_message(self) -> str:
        return self.pattern.format(
            "DEBUG",
            self.get_guild_name(),
            self.get_message_author(),
            self.get_message_content()
        )

# ================================================================================
# Error message class which inherits from Base message class.
# ================================================================================

class ErrorLogMessage(BaseLogMessage):
    def __init__(self, message: discord.Message) -> None:
        super().__init__(message)

    # Formats the logging pattern.
    # RETURN: str => Returns the formated string for logging.
    def get_message(self) -> str:
        return self.pattern.format(
            "ERROR",
            self.get_guild_name(),
            self.get_message_author(),
            self.get_message_content()
        )

def log_to_stdout(log_message: BaseLogMessage):
    log_message.print_message()

def log_to_file(log_message: BaseLogMessage):
    writer = FileWriter(path=".", filename="discord.log", encoding="utf-8")
    writer.write(log_message.get_message())

def log(log_message: BaseLogMessage):
    log_to_stdout(log_message)
    log_to_file(log_message)