import time
import discord

from typing import Union
from cprint import cprint

from src.handle import FileWriter 

# ================================================================================
# Base message class which inherits from discord's Message class
# ================================================================================

class BaseLogMessage:
    def __init__(self, message: discord.Message) -> None:
        self.message = message
        self.pattern = f"[{time.ctime()}] " + "[{}] : " + f"[{self.message.guild.name}] {self.message.author.display_name} sent => {self.message.content}\n" # Log level, guild, author, message

    # virtual function to be overriden by child classes
    def getMessage(self):
        raise NotImplementedError("Must be overriden by child class")
    
    # prints the message to stdout
    def printMessage(self):
        if isinstance(self, DebugLogMessage):
            cprint.info(self.getMessage())
        elif isinstance(self, ErrorLogMessage):
            cprint.err(self.getMessage())
        
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
        return self.pattern.format('DEBUG')

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
        return self.pattern.format('ERROR')

'''
Logs message to stdout.
'''
def logToStdout(logMessage: Union[BaseLogMessage, str]):
    if isinstance(logMessage, str): print(logMessage)
    else: logMessage.printMessage()

'''
Logs message to a file specified by filename parameter.
'''
def logToFile(logMessage: Union[BaseLogMessage, str]):
    writer = FileWriter(path=".", filename="discord.log", encoding="utf-8")
    if isinstance(logMessage, str): writer.write(logMessage + '\n')
    else: writer.write(logMessage.getMessage())

'''
Wrapper around both function.
'''
def log(logMessage: Union[BaseLogMessage, str]):
    logToStdout(logMessage)
    logToFile(logMessage)
