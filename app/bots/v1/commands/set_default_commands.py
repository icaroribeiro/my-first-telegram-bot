from aiogram import Bot, types

from app.bots.v1.commands.languages.en.commands_en import get_commands_en
from app.bots.v1.commands.languages.pt_br.commands_pt_br import get_commands_pt_br


async def set_default_commands(bot: Bot):
    command_configurations = [
        (get_commands_en, "en"),    
        (get_commands_pt_br, "pt"),
    ]

    scope = types.BotCommandScopeAllPrivateChats()

    for getter_func, lang_code in command_configurations:
        commands = getter_func()
        await bot.set_my_commands(commands, scope=scope, language_code=lang_code)
