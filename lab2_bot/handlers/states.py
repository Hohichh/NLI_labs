from aiogram.fsm.state import State, StatesGroup


class FSMCorpus(StatesGroup):
    send_docx_file = State()
    delete = State()
    view = State()
    stats_word_input = State()
    current_doc = State()
