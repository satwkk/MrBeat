from discord.ext import commands

# Voice client related exceptions
class InvokerClientError(commands.CommandError):
    pass

class VoiceClientAlreadyActive(commands.CommandError):
    pass

class VoiceClientNone(commands.CommandError):
    pass

class AlreadyPlayingAudio(commands.CommandError):
    pass

# Queue related exceptions
class QueueNotEmpty(commands.CommandError):
    pass

class QueueIsEmpty(commands.CommandError):
    pass

# URL Validation related exceptions
class InvalidSongUrl(commands.CommandError):
    pass

class InvalidStreamingUrl(commands.CommandError):
    pass