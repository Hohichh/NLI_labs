import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from handlers import FSMCorpus
from services import parse_add_word, CorpusDoc
from lexicon import LEXICON_RU

doc_router = Router()

@doc_router.message(StateFilter(FSMCorpus.current_doc))
async def process_stats(message: Message, state: FSMContext):
    word = parse_add_word(message.text)

    if not word:
        await message.answer(text="Некорректный ввод. Нажмите /help для справки.")
        return
    
    data = await state.get_data()
    doc: CorpusDoc = data.get("curr_doc")

    stats: str = doc.pretty_print_stats(word)
    await message.answer(text=stats)
    await state.set_state(default_state)
    