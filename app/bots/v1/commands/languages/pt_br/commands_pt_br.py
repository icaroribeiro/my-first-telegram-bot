from aiogram import types


def get_commands_pt_br() -> list[types.BotCommand]:
    commands = [
        types.BotCommand(
            command="/start", description="Iniciar o diálogo principal do bot"
        ),
        types.BotCommand(command="/help", description="Ver comandos e instruções"),
        types.BotCommand(command="/exit", description="Sair do diálogo"),
    ]
    return commands
