from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from io import BytesIO
from docx import Document

from lexicon import LEXICON_RU
from .states import FSMWorkWithDict
from services import Dictionary, Lexeme
from services import parse_adjective_rules, parse_noun_rules, parse_verb_rules


dict_router = Router()

@dict_router.message(Command(commands='show_dictionary'))
async def process_show_dictionary_command(message: Message, state: FSMContext):
    data = await state.get_data()
    dictionary : Dictionary = data.get('dictionary')
    if not dictionary:
        await message.answer("Словарь не загружен. Создайте его на /create_dictionary")
        return
    await message.answer(text=dictionary.pretty_print_keys())

# Хендлер для команды /create_dictionary
@dict_router.message(Command(commands='create_dictionary'), StateFilter(default_state))
async def process_create_dictionary_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=LEXICON_RU["request_word_file"]
    )
    await state.set_state(FSMWorkWithDict.send_word_file)

# Хендлер для приёма word-файла
@dict_router.message(F.document, StateFilter(FSMWorkWithDict.send_word_file))
async def process_word_file_sent(message: Message, state: FSMContext):
    if message.document.mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        # Скачиваю файл и преобразовываю в doc для работы
        file_id = message.document.file_id
        file = await message.bot.get_file(file_id)
        file_bytes = await message.bot.download_file(file.file_path)
        doc_stream = BytesIO(file_bytes.read())

        doc = Document(doc_stream) #получаем документ 
        dictionary = Dictionary(doc)
         
        # Сохраняем ВЕСЬ объект словаря в состоянии
        await state.update_data(
            dictionary=dictionary,
            words_list=list(dictionary.dictionary.keys())  # сохраняем список слов отдельно
        )
        
        # Показываем пользователю список слов
        await message.answer(
            text=dictionary.pretty_print_keys() + "\n" + LEXICON_RU["word_file_received"] 
        )

        await state.set_state(FSMWorkWithDict.select_word)
    else:
        await message.answer(
            text=LEXICON_RU["wrong_file_format"]
        )

# Хендлер для случая, когда в состоянии send_word_file прислано не документ
@dict_router.message(StateFilter(FSMWorkWithDict.send_word_file))
async def warning_not_word_file(message: Message):
    await message.answer(
        text=LEXICON_RU["not_word_file"]
    )

# Хендлер для выбора слова (ожидаем номер слова)
@dict_router.message(StateFilter(FSMWorkWithDict.select_word), 
                F.text.isdigit())
async def process_word_selected(message: Message, state: FSMContext):
    data = await state.get_data()
    word_list = data.get('words_list', []) 

    word_number = int(message.text)

    if 1 <= word_number <= len(word_list):
        selected_word = word_list[word_number - 1]  
        
        await state.update_data(
            selected_word=selected_word,
            selected_word_number=word_number
        )

        dictionary: Dictionary = data.get('dictionary')
        word_info : Lexeme = dictionary.dictionary[selected_word]
        print('selected_word = ', selected_word )
        
        word_info_str : str = word_info.pretty_print()

        await message.answer(LEXICON_RU["word_selected"].format(
            selected_word=selected_word,
            word_info=word_info_str
        ))

        await message.answer(text=LEXICON_RU["enter_rules_prompt"])
        await state.set_state(FSMWorkWithDict.select_rules)
    else:
        await message.answer(text=LEXICON_RU["invalid_word_number"])

@dict_router.message(StateFilter(FSMWorkWithDict.select_word))    
async def process_non_number_input(message: Message):
    await message.answer(
            text=LEXICON_RU["not_a_number"]
        )
    
# Хендлер для ввода правил
@dict_router.message(StateFilter(FSMWorkWithDict.select_rules))
async def process_rules_entered(message: Message, state: FSMContext):

    data = await state.get_data()
    selected_word : str = data.get('selected_word') #обрабатываем слово, выбранное юзером.
    dictionary : Dictionary = data.get('dictionary')
    
    try:
        lexeme : Lexeme = dictionary.dictionary[selected_word]
        pos = lexeme.pos

        if pos == "NOUN" or pos == "PROPN":
            morph_params = parse_noun_rules(message.text)
        elif pos == "VERB":
            morph_params = parse_verb_rules(message.text)
        elif pos in {"ADJ", "ADV"}:
            morph_params = parse_adjective_rules(message.text)
        else:
            await message.answer("Для этой части речи генерация форм не поддерживается")
            return
        
        
        new_form = dictionary.generate_form(selected_word, morph_params)
        value = dictionary.dictionary.pop(selected_word)
        dictionary.dictionary[new_form] = value
        await message.answer(f"Новая форма слова: {new_form}")
        await state.set_state(FSMWorkWithDict.select_word)
        await message.answer("Введите номер слова, чтобы продолжить работу со словарём"
        " или отмените операцию на /cancel")
 
    except ValueError as e:
        await message.answer(f"Ошибка ввода: {str(e)}")
        print(e.with_traceback())
    except KeyError:
        await message.answer("Ошибка: не удалось сгенерировать форму. Проверьте параметры.")
    except Exception as e:
        import traceback
        exception_traceback = traceback.format_exc()
        print(exception_traceback)
        await message.answer(f"Произошла ошибка: {str(e)}")
        await state.clear()


@dict_router.message(Command(commands='return_to_dictionary'), StateFilter(default_state))
async def process_return_to_dictionary_command(message: Message, state: FSMContext):
    data = await state.get_data()
    dictionary: Dictionary = data.get("dictionary")
    if not dictionary or not dictionary.dictionary:
        await message.answer("Словарь не загружен. Создайте его на /create_dictionary")
        return
    await state.update_data(words_list=list(dictionary.dictionary.keys()))
    await message.answer(text=LEXICON_RU['return_to_dictionary'])
    await state.set_state(FSMWorkWithDict.select_word)
    
