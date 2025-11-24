from aiogram import types


def get_commands_en() -> list[types.BotCommand]:
    commands = [
        types.BotCommand(command="/start", description="Start the main bot dialog"),
        types.BotCommand(
            command="/help", description="View bot commands and instructions"
        ),
        types.BotCommand(
            command="/exit", description="Exit or cancel the current task"
        ),
    ]
    return commands
