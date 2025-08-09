from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from services.book_service import BookService
from infrastructure.database import get_session
from repositories.book_repository import BookRepository
from infrastructure.file_storage import FileStorage

#FSM
class SearchStates(StatesGroup):
    waiting_for_query = State()
#Кнопки
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Найти книгу")],
            [KeyboardButton(text="Загрузить книгу")],
            [KeyboardButton(text="Help")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard
#Отмена поиска
def get_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отмена")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def register_handlers(dp: Dispatcher) -> None:
    print("Registering handlers in start.py") #Откладка

    # Start
    @dp.message(Command(commands=['start']))
    async def handle_start(message: types.Message, state: FSMContext):
        print(f"Received /start from {message.from_user.id}")
        await state.clear()
        await message.reply(
            "Добро пожаловать в BooxBot! Выбери действие:",
            reply_markup=get_main_keyboard()
        )

#help
    @dp.message(lambda message: message.text == "Help")
    async def send_help(message: types.Message):
        print(f"Received /help from {message.from_user.id}")  # Для отладки
        await message.reply(
        "Справка:\n"
            "Используйте кнопки для навигации:\n"
            " - Найти книгу: Поиск книг по названию или автору\n"
            " - Загрузить книгу: Добавление новой книги\n"
            " - Help: Получить эту справку",
            reply_markup=get_main_keyboard()
        )

#list
    #@dp.message(Command(commands=['list']))
    #async def list_books(message: types.Message):
        #print(f"Received /list from {message.from_user.id}")  # Для отладки
        #async for session in get_session():
            #book_service = BookService(BookRepository(session), FileStorage())
            #books = await book_service.get_all_books()
            #if not books:
                #await message.reply("No books available.", reply_markup=get_main_keyboard())
                #return
            #response = "\n".join(
                #[f"{book.title} by {book.author} ({book.format.upper()})" for book in books]
            #)
            #await message.reply(f"Books:\n{response}", reply_markup=get_main_keyboard())

    #Найти книгу
    @dp.message(lambda message: message.text == "Найти книгу")
    async def search_book(message: types.Message, state: FSMContext):
        print(f"Received search request from {message.from_user.id}")  # Для отладки
        await state.set_state(SearchStates.waiting_for_query)
        await message.reply(
            "Введите название или автора для поиска.",
            reply_markup=get_main_keyboard()
        )

    #Обработка поискового запроса
    @dp.message(SearchStates.waiting_for_query)
    async def process_search_query(message: types.Message, state: FSMContext):
        print(f"Received search request from {message.from_user.id}: {message.text}")
        if message.text == "Отмена":
            await state.clear()
            await message.reply(
                "Поиск отменен.",
                reply_markup=get_main_keyboard()
            )
            return

        query = message.text.strip()
        try:
            async for session in get_session():
                book_service = BookService(BookRepository(session), FileStorage())
                books = await book_service.search_books(query)
                print(f"Books returned from search_books: {type(books)} {books}") #Добавленная проверочная отладка
                if not books:
                    await message.reply(
                        f"Книги по запросу '{query}' не найдены.",
                        reply_markup=get_main_keyboard()
                    )
                else:
                    response = "\n".join(
                        [f"{book.title} by {book.author} ({book.format.upper()}" for book in books]
                    )
                    await message.reply(
                        f"Найдены книги:\n{response}",
                        reply_markup=get_main_keyboard()
                    )
        except Exception as e:
            print(f"Error in search_books: {str(e)}") #Откладка
            await message.reply(f"Ошибка при поиске книг: {str(e)}", reply_markup=get_main_keyboard())
        await state.clear()

    # Заглушка для кнопки "Загрузить книгу"
    @dp.message(lambda message: message.text == "Загрузить книгу")
    async def add_book(message: types.Message):
        print(f"Received add book request from {message.from_user.id}")  #Отладка
        await message.reply(
            "Функция добавления книги пока в разработке. Отправьте файл книги.",
            reply_markup=get_main_keyboard()
        )

    @dp.message()
    async def handle_any_message(message: types.Message, state: FSMContext):
        print(f"Received any message from {message.from_user.id}: {message.text}") #Откладка
        await state.clear()
        await message.reply(
            "Добро пожаловать в Book Bot! Выберите действие:",
            reply_markup=get_main_keyboard()
        )