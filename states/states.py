from aiogram.dispatcher.filters.state import State, StatesGroup
# States
class Language(StatesGroup):
    language = State()

class calculate_datas(StatesGroup):
    cur = State()
    electr = State()