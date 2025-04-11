from aiogram import Router
from aiogram.types import Message


default_router = Router()

@default_router.message()
async def process_everything(message: Message):
    await message.answer(text="Ваш запрос не корректен. Следуйте инструкциям в /help")