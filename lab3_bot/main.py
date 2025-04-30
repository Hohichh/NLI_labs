import asyncio
import logging

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from configs import Config, load_config, set_main_menu
from handlers import util_router, main_route, default_router



logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    config: Config = load_config()

    bot = Bot(
        token=config.tg_Bot.token
      )
    mem_state = MemoryStorage()

    dp = Dispatcher(storage=mem_state)
    dp.startup.register(set_main_menu)
    dp.include_routers(util_router, main_route, default_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())