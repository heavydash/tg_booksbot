
from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Message
from services.book_service import BookService

class BookServiceMiddleware(BaseMiddleware):
    def __init__(self, book_service: BookService):
        super().__init__()
        self.book_service = book_service

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        data["book_service"] = self.book_service
        return await handler(event, data)