import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN


logger = logging.getLogger(__name__)


class BotConfig:
    """Конфигурация Bot и Dispatcher"""

    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        logger.info("BotConfig initialised")

    async def close(self):
        """Закрыть сессию бота"""
        await self.bot.session.close()
        logger.info("Bot seeeion closed")


