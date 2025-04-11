from aiogram import Bot
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием
    main_menu_commands = [
        BotCommand(command='/start', description='Запустить бота'),
        BotCommand(command='/help', description='Справка по работе бота'),
        BotCommand(command='/create_dictionary', description='Начать работу со словарем'),
        BotCommand(command='/cancel', description='Отменить текущее действие'),
        BotCommand(command='/return_to_dictionary', description='Вернуться к текущему словаря'),
        BotCommand(command='/show_dictionary', description='Отобразить словарь'),
        BotCommand(command='/add_word', description='Добавить слово в словарь'),
        BotCommand(command='/filter', description='Фильтрация по частям речи'),
        BotCommand(command='/search', description='Поиск слов с одной леммой')
    ]
    
    await bot.set_my_commands(main_menu_commands)