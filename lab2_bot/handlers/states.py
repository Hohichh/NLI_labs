from aiogram.fsm.state import State, StatesGroup


class FSMCorpus(StatesGroup):
    send_docx_file = State()
    title_input = State()
    author_input = State()
    delete = State()
    view = State()
    stats_word_input = State()
    examples_word_input = State()
    current_doc = State()
    current_doc_stats = State()
    current_doc_examples = State()
