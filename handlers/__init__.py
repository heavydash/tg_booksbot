from aiogram import Dispatcher
from .start import register_handlers as register_start_handlers


def register_handlers(dp: Dispatcher):
    """Регистрация всех handlers"""
    register_start_handlers(dp)