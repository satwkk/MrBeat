import time
import discord

from typing import Union
from cprint import cprint

from src.handle import FileWriter

# ================================================================================
# Base message class which inherits from discord's Message class
# ================================================================================

class BaseLogMessage():
    def __init__(self, message: discord.Message) -> None:
        self.message = message
        self.pattern = f"[{time.ctime()}] " + "[{}] : [{}] {} sent => {}\n" # Log level, guild, author, message
    
    # virtual function to be overriden by child classes
    def getMessage(self):
        raise NotImplementedError("Must be overriden by child class")
    
    # prints the message to stdout
    def printMessage(self):
        if isinstance(self, DebugLogMessage):
            cprint.info(self.getMessage())
        elif isinstance(self, ErrorLogMessage):
            cprint.err(self.getMessage())
        
    # returns name of the discord channel
    def getGuildName(self):
        return self.message.guild.name

    # returns the name of the author who invoked the command
    def getMessageAuthor(self):
        return self.message.author.display_name

    # returns the content of the message
    def getMessageContent(self):
        return self.message.content
    
# ================================================================================
# Debug message class which inherits from Base message class.
# ================================================================================

class DebugLogMessage(BaseLogMessage):
    def __init__(self, message: discord.Message) -> None:
        super().__init__(message)

    '''
    Formats the logging pattern.
    @param: None
    '''
    def getMessage(self) -> str:
        return self.pattern.format(
            "DEBUG",
            self.getGuildName(),
            self.getMessageAuthor(),
            self.getMessageContent()
        )

'''
Error message class which inherits from Base message class.
'''
class ErrorLogMessage(BaseLogMessage):
    def __init__(self, message: discord.Message) -> None:
        super().__init__(message)

    '''
    Formats the logging pattern.
    @param: None
    '''
    def getMessage(self) -> str:
        return self.pattern.format(
            "ERROR",
            self.getGuildName(),
            self.getMessageAuthor(),
            self.getMessageContent()
        )

'''
Logs message to stdout.
'''
def log_to_stdout(log_message: Union[BaseLogMessage, str]):
    if isinstance(log_message, str):
        print(log_message)
    else:
        log_message.printMessage()

'''
Logs message to a file specified by filename parameter.
'''
def log_to_file(log_message: Union[BaseLogMessage, str]):
    writer = FileWriter(path=".", filename="discord.log", encoding="utf-8")
    if isinstance(log_message, str):
        writer.write(log_message + '\n')
    else:
        writer.write(log_message.getMessage())

'''
Wrapper around both function.
'''
def log(log_message: BaseLogMessage):
    log_to_stdout(log_message)
    log_to_file(log_message)