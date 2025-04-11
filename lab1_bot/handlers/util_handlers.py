from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon import LEXICON_RU
from .states import FSMWorkWithDict



util_router = Router()


# /start - запуск бота
@util_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_RU['start']
    )

# /cancel - отмена в дефолт состоянии
@util_router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text=LEXICON_RU["cancel_state_out"]
    )
# /cancel - отмена внутри состояний
@util_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_FSM_command(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU['cancel_state_in']
    )
    await state.set_state(default_state)

# Хендлер для команды /help вне состояний
@util_router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(
        text=LEXICON_RU["help_state_out"]
    )

# Хендлеры для команды /help в разных состояниях
@util_router.message(Command(commands='help'), StateFilter(FSMWorkWithDict.send_word_file))
async def process_help_send_word_file(message: Message):
    await message.answer(
        text=LEXICON_RU["help_send_word_file"]
    )

@util_router.message(Command(commands='help'), StateFilter(FSMWorkWithDict.select_word))
async def process_help_select_word(message: Message):
    await message.answer(
        text=LEXICON_RU["help_select_word"]
    )

@util_router.message(Command(commands='help'), StateFilter(FSMWorkWithDict.select_rules))
async def process_help_select_rules(message: Message):
    await message.answer(
        text=LEXICON_RU["help_select_rules"]
    )
