from aiogram.fsm.state import State, StatesGroup


class BMIDialogSG(StatesGroup):
    greeting = State()
    age = State()
    height = State()
    weight = State()
    bmi = State()
    finish = State()
