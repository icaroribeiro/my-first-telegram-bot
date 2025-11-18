from aiogram import types

def get_commands_pt_br() -> list[types.BotCommand]:
    commands = [
        types.BotCommand(command="/start", description="Iniciar o bot"),
        types.BotCommand(command="/help", description="Ajuda"),
    ]
    return commands