from aiogram.fsm.state import State, StatesGroup


class SetProfile(StatesGroup):
    START = State()
    CREATE = State()
    NAME = State()
    PREVIEW = State()
    FINISH = State()
