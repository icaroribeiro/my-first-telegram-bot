from aiogram import types

def get_commands_en() -> list[types.BotCommand]:
    commands = [
        types.BotCommand(command="/start", description="Start the bot"),
        types.BotCommand(command="/help", description="Help"),
    ]
    return commands
