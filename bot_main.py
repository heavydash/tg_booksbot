import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

from handlers.start import register_handlers

register_handlers(dp)

if __name__ == '__main__':
    import asyncio
    async def main():
        await dp.start_polling(bot)
    asyncio.run(main())
