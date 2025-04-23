import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from .states import FSMCorpus
from services import parse_add_word, CorpusDoc
from lexicon import LEXICON_RU

doc_router = Router()


@doc_router.message(StateFilter(FSMCorpus.current_doc, 
                                FSMCorpus.current_doc_examples,
                                FSMCorpus.current_doc_stats), Command(commands="examples"))
async def process_examples_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU["examples_word_input"])
    await state.set_state(FSMCorpus.current_doc_examples)

@doc_router.message(StateFilter(FSMCorpus.current_doc_examples))
async def process_examples_input(message: Message, state: FSMContext):
    word = message.text
    data = await state.get_data()
    curr_doc: CorpusDoc = data.get("curr_doc")

    stats = await curr_doc.pretty_print_concordance(word)
    await message.answer(text=stats)

@doc_router.message(StateFilter(FSMCorpus.current_doc, 
                                FSMCorpus.current_doc_examples,
                                FSMCorpus.current_doc_stats), Command(commands="statistics"))
async def process_examples_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU["stats_word_input"])
    await state.set_state(FSMCorpus.current_doc_stats)

@doc_router.message(StateFilter(FSMCorpus.current_doc_stats))
async def process_examples_input(message: Message, state: FSMContext):
    word = parse_add_word(message.text)

    if not word:
        await message.answer(text="Некорректный ввод. Нажмите /help для справки.")
        return
    
    data = await state.get_data()
    curr_doc: CorpusDoc = data.get("curr_doc")

    stats = await curr_doc.pretty_print_stats(word)
    await message.answer(text=stats)