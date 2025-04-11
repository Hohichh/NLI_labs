from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state


from lexicon import LEXICON_RU
from .states import FSMWorkWithDict
from services import Dictionary, parse_add_word, nlp


add_router = Router()


@add_router.message(Command(commands='add_word'))
async def process_add_command(message: Message, state: FSMContext):
    data = await state.get_data()
    dictionary: Dictionary = data.get('dictionary')

    if not dictionary:
        await message.answer(text="Словарь не загружен. Создайте его на /create_dictionary.")
        await state.set_state(default_state)
        return
    
    await message.answer(text=LEXICON_RU['add_word'])
    await state.set_state(FSMWorkWithDict.add_word)

@add_router.message(StateFilter(FSMWorkWithDict.add_word))
async def process_add_word_input(message: Message, state: FSMContext):

    added_word = parse_add_word(message.text)
    if not added_word:
        await message.answer(text=LEXICON_RU['incorrect_add_word_input'])
        return
    
    data = await state.get_data()
    dictionary: Dictionary = data.get('dictionary')
    dictionary.add_word(added_word)
    await message.answer(text='Слово успешно добавлено')
    await state.set_state(default_state)
    
@add_router.message(Command(commands='filter'))
async def process_filter_command(message: Message, state: FSMContext):
    data = await state.get_data()
    dictionary: Dictionary = data.get('dictionary')

    if not dictionary:
        await message.answer(text="Словарь не загружен. Создайте его на /create_dictionary.")
        await state.set_state(default_state)
        return

    pos_list_str = ( "\n\n"
        "1 - Существительное (Noun)\n"
        "2 - Глагол (Verb)\n"
        "3 - Прилагательное\n"
        "4 - Наречие\n"
    )
    await message.answer(text=LEXICON_RU['filter'].format(pos_list=pos_list_str))
    await state.set_state(FSMWorkWithDict.filter_by_pos)

@add_router.message(StateFilter(FSMWorkWithDict.filter_by_pos), F.text.isdigit())
async def process_filter_input(message: Message, state: FSMContext):
    num = (int)(message.text)
    pos_text: str
    pos_tag: str
    if 1 <= num <= 4:
        if num == 1: 
            pos_text = "Существительные"
            pos_tag = "NOUN"
        elif num == 2: 
            pos_text = "Глаголы"
            pos_tag = "VERB"
        elif num == 3: 
            pos_text = "Прилагательные"
            pos_tag = "ADJ"
        elif num == 4: 
            pos_text = "Наречия"
            pos_tag = "ADV"

        await message.answer(text=f"Все {pos_text}:")

        data = await state.get_data()
        dictionary: Dictionary = data.get('dictionary')
        word_by_pos_list = []
        for key, value in dictionary.dictionary.items():
            if pos_tag == "NOUN":
                if value.pos == "NOUN" or value.pos == "PROPN":
                    word_by_pos_list.append(key)
            else:
                if value.pos == pos_tag:
                    word_by_pos_list.append(key)

        str_word_list = "\n".join(f"{i}. {word}" for i, word in enumerate(word_by_pos_list, start=1))
        await message.answer(text=str_word_list + "\n Выберите номер слова, для которого желаете сгенерировать словоформу. /cancel")
        await state.update_data(
            words_list=word_by_pos_list
        )
        await state.set_state(FSMWorkWithDict.select_word)
        return

    await message.answer(text="Введите номер из списка (1-4).")   

@add_router.message(StateFilter(FSMWorkWithDict.filter_by_pos))
async def process_incorrect_filter_input(message: Message, state:FSMContext):
    data = await state.get_data()
    dictionary: Dictionary = data.get('dictionary')

    if not dictionary:
        await message.answer(text="Словарь не загружен. Создайте его на /create_dictionary.")
        await state.set_state(default_state)
        return
    
    await message.answer(text="Введите номер части речи из списка, по которой хотите произвести фильтрацию.")
    
@add_router.message(Command(commands='search'))
async def process_search_command(message: Message, state: FSMContext):
    data = await state.get_data()
    dictionary: Dictionary = data.get('dictionary')

    if not dictionary:
        await message.answer(text="Словарь не загружен. Создайте его на /create_dictionary.")
        await state.set_state(default_state)
        return

    await message.answer(text=LEXICON_RU['search'])
    await state.set_state(FSMWorkWithDict.search_words)

@add_router.message(StateFilter(FSMWorkWithDict.search_words))
async def process_search_words_input(message: Message, state: FSMContext):
    cognate_words = []
    data = await state.get_data()
    dictionary: Dictionary = data.get("dictionary")

    tokens = nlp(message.text)
    curr_word = tokens[0]

    for key, value in dictionary.dictionary.items():
        if curr_word.lemma_ == value.lemma:
            cognate_words.append(key)
    
    if not cognate_words:
        await message.answer(text="В словаре нет слов, с такой же леммой.")
        return

    str_cognate_words = "\n".join(f"{i}. {word}" for i, word in enumerate(cognate_words, start=1))
    await message.answer(text=f"Слова с леммой, как у {curr_word}:\n" + str_cognate_words)
    message.answer(text="Выберите номер слова, для которого желаете сгенерировать словоформу. /cancel")
    await state.update_data(
        words_list=cognate_words
    )
    await state.set_state(FSMWorkWithDict.select_word)