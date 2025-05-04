from aiogram import Bot
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/start', description='Запустить бота'),
        BotCommand(command='/help', description='Справка по работе бота'),
        BotCommand(command='/load_text', description='Загрузить текст'),
        BotCommand(command='/view_text', description='Просмотреть текст'),
        BotCommand(command='/get_trees', description='Просмотреть синтаксические деревья'),
        BotCommand(command='/get_tree', description='Посмотреть 1 дерево'),
        BotCommand(command='/get_semantic_info', description='Семантические сведения о слове'),
        BotCommand(command='/get_predicates', description='Получить предикаты'),
        BotCommand(command='/cancel', description='Отменить текущее действие')
    ]
    
    await bot.set_my_commands(main_menu_commands)