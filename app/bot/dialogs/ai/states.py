from aiogram.fsm.state import State, StatesGroup

class AIStates(StatesGroup):
    START = State()
    INPUT = State()
    PREVIEW = State()
    RESULT = State()