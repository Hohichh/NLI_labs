import asyncio
from io import BytesIO
from docx import Document

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon import LEXICON_RU
from handlers import FSMCorpus
from services import CorpusDoc, CorpusManager, parse_add_word


corpus_router = Router()

@corpus_router.message(Command(commands="/create_document"))
async def process_create_commnad(message: Message, state: FSMContext):
    data = await state.get_data()
    corpus = data.get("corpus")

    if not corpus:
        message.answer("Выберите /start, чтобы начать работу с корпусным менеджером")
        return
    
    await message.answer(text=LEXICON_RU["request_word_file"])
    await state.set_state(FSMCorpus.send_docx_file)

@corpus_router.message(F.document, StateFilter(FSMCorpus.send_docx_file))
async def process_word_file_input(message: Message, state:FSMContext):
    mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    if message.document.mime_type != mime:
        await message.answer(
            text=LEXICON_RU["wrong_file_format"]
        )
        return

    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_bytes = await message.bot.download_file(file.file_path)
    doc_stream = BytesIO(file_bytes.read())

    doc = Document(doc_stream) #получаем word-документ 
    text_doc = CorpusDoc(doc)
        
    # Сохраняем ВЕСЬ объект словаря в состоянии
    data = await state.get_data()
    corpus_manager: CorpusManager = data.get("corpus") #Выгружаем сам менеджер

    if not corpus_manager.add_doc(text_doc): #если что-то пошло не так при добавлении
        await message.answer(text=LEXICON_RU["undefined_error"])
        return 
    
    await state.update_data(corpus=corpus_manager)
    await message.answer(text=LEXICON_RU["word_file_received"])
    await state.set_state(default_state)
        
    
@corpus_router.message(StateFilter(FSMCorpus.send_docx_file))
async def warning_not_word_file(message: Message):
    await message.answer(
        text=LEXICON_RU["not_word_file"]
    )
    

@corpus_router.message(Command(commands="delete_document"))
async def process_delete_commnad(message: Message, state:FSMContext):
    data = await state.get_data()
    corpus_manager: CorpusManager = data.get("corpus")

    if not corpus_manager:
        message.answer("Выберите /start, чтобы начать работу с корпусным менеджером")
        return
    
    title_list = corpus_manager.get_docs_name_list()
    numeric_text_list = ""
    for i, title in enumerate(title_list, start=1):
        numeric_text_list += f"{i}. {title}\n"
    
    await message.answer("Введите номер текста из списка: \n" + numeric_text_list)
    await state.set_state(FSMCorpus.delete)

@corpus_router.message(StateFilter(FSMCorpus.delete), F.text.isdigit())
async def process_delete_text(message: Message, state: FSMContext):
    data = await state.get_data()
    corpus_manager: CorpusManager = data.get("corpus")

    if not corpus_manager.delete_doc(int(message.text)-1):
        message.answer(text=LEXICON_RU["invalid_doc_number"])
        return

    await state.update_data(corpus=corpus_manager)
    await message.answer(text=LEXICON_RU["successful_delete"])


@corpus_router.message(Command(commands="view_document"))
async def process_view_commnad(message: Message, state: FSMContext):
    data = await state.get_data()
    corpus_manager: CorpusManager = data.get("corpus")

    if not corpus_manager:
        message.answer("Выберите /start, чтобы начать работу с корпусным менеджером")
        return
    
    title_list = corpus_manager.get_docs_name_list()
    numeric_text_list = ""
    for i, title in enumerate(title_list, start=1):
        numeric_text_list += f"{i}. {title}\n"
    
    await message.answer("Введите номер текста из списка: \n" + numeric_text_list)
    await state.set_state(FSMCorpus.view)

@corpus_router.message(StateFilter(FSMCorpus.view), F.text.isdigit())
async def process_view_text(message: Message, state: FSMContext):
    data = await state.get_data()
    corpus_manager: CorpusManager = data.get("corpus")
    doc = corpus_manager.get_doc(int(message.text)-1)
    if not doc:
        await message.answer(LEXICON_RU["invalid_doc_number"])
        return
    
    await message.answer(text=(
        "{title}\n"
        "by {author}\n"
        "topic: {topic}\n"
        "{text}"
    ).format(
        title=doc.title,
        author=doc.author,
        topic=doc.topic,
        text=doc.text
    ))

    await message.answer(text=LEXICON_RU["stats_word_input"])
    await state.update_data(curr_doc=doc)
    await state.set_state(FSMCorpus.current_doc)

@corpus_router.message(StateFilter(FSMCorpus.delete, FSMCorpus.view))
async def process_non_number_input(message: Message):
    await message.answer(
            text=LEXICON_RU["not_a_number"]
        )
    
@corpus_router.message(Command(commands="statistics"), StateFilter(default_state))
async def process_stats_commnad(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU["stats_word_input"])
    await state.set_state(FSMCorpus.stats_word_input)

@corpus_router.message(StateFilter(FSMCorpus.stats_word_input))
async def process_stats_input(message: Message, state: FSMContext):
    word = parse_add_word(message.text)

    if not word:
        await message.answer(text="Некорректный ввод. Нажмите /help для справки.")
        return
    
    data = await state.get_data()
    corpus_manager: CorpusManager = data.get("corpus")

    stats = corpus_manager.pretty_print_stats(word)
    await message.answer(text=stats)
