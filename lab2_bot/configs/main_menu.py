from aiogram import Bot
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием
    main_menu_commands = [
        BotCommand(command='/start', description='Запустить бота'),
        BotCommand(command='/help', description='Справка по работе бота'),
        BotCommand(command='/add_text', description='Добавить текст в корпус'),
        BotCommand(command='/delete_text', description='Удалить текст из корпуса'),
        BotCommand(command='/show_text', description='Просмотр информации по тексту'),
        BotCommand(command='/statistics', description='Статистическая информация по слову'),
        BotCommand(command='/cancel', description='Отменить текущее действие'),
    ]
    
    await bot.set_my_commands(main_menu_commands)