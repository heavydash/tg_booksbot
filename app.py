import logging
from aiogram.types import BotCommand, BotCommandScopeDefault

from bot_config import BotConfig
from infrastructure.database import init_db
from handlers import register_handlers

logger = logging.getLogger(__name__)

class Application:
    """Главное приложение бота"""


    def __init__(self):
        self.config = BotConfig()
        self.bot = self.config.bot
        self.dp = self.config.dp
        logger.info("Application initialised")

    async def _set_commands(self):
        """Установить меню команд бота"""
        commands = [
            BotCommand(command="start", description="Start work with booxbot"),
            BotCommand(command="search", description="Finder"),
            BotCommand(command="history", description="Your history"),
            BotCommand(command="help", description="Info"),
        ]
        await self.bot.set_my_commands(commands, BotCommandScopeDefault())
        logger.info("Commands have been installed")

    async def init(self):
        """Инициализация приложения"""
        logger.info("Apllication init")

        # Инициализация БД
        try:
            logger.info("DB initialisation")
            await init_db()
            logger.info("DB has been initialised")
        except Exception as e:
            logger.error(f"Fault of initialisation of DB: {e}")
            raise

        # Регистрация handlers
        try:
            logger.info("Handlers registration")
            register_handlers(self.dp)
            logger.info("Handlers has been registered")
        except Exception as e:
            logger.error(f"Fault of registration of handlers: {e}")
            raise

        # Установка команд
        try:
            await self._set_commands()
        except Exception as e:
            logger.error(f"Fault of installing commands: {e}")

    async def run(self):
        """Запустить бота"""

        try:
            logger.info("Bot has been raised and listening")
            await self.dp.start_polling(
                self.bot,
                allowed_updates=self.dp.resolve_used_update_types()
            )
        except KeyboardInterrupt:
            logger.info("Bot has been stopped by user")
        except Exception as e:
            logger.error(f"Fault of working of bot: {e}")
        finally:
            await self.config.close()

    async def start(self):
        """Полный цикл: инициализация + запуск"""
        await self.init()
        await self.run()
