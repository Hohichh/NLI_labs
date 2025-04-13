from aiogram.fsm.state import State, StatesGroup


class FSMCorpus(StatesGroup):
    send_docx_file = State()
    select_text = State()
    stats_word_input = State()
