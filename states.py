from aiogram.dispatcher.filters.state import StatesGroup, State

class MyStates(StatesGroup):
    set_first = State()
    set_second = State()
    set_third = State()