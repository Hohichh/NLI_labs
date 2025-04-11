from aiogram.fsm.state import State, StatesGroup


class FSMWorkWithDict(StatesGroup):
    send_word_file = State()
    select_word = State()
    select_rules = State()
    add_word = State()
    filter_by_pos = State()
    search_words = State()