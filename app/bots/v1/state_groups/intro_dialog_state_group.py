from aiogram.fsm.state import State, StatesGroup


class IntroDialogSG(StatesGroup):
    greeting = State()
    age = State()
    finish = State()
