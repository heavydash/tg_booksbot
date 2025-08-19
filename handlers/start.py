from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.keyboards import get_main_keyboard, get_cancel_keyboard
from aiogram.fsm.state import default_state

router = Router()
# Start
@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.reply(
        "Добро пожаловать в BooxBot! Выбери действие:",
        reply_markup=get_main_keyboard()
    )

#Help
@router.message(F.text=="Help", default_state)
async def cmd_help(message: types.Message) -> None:
    await message.reply(
        "Справка:\n"
        "- Найти книгу: Поиск книг по названию или автору\n"
        "- Загрузить книгу: Добавление новой книги\n"
        "- Help: Получить эту справку",
        reply_markup=get_main_keyboard()
    )
#Отмена
@router.message(F.text=="Отмена")
async def cancel_action(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Действие отменено.", reply_markup=get_main_keyboard())

@router.message(F.text.not_in(["Найти  книгу", "Загрузить книгу", "Help"]), default_state)
async def handle_any_message(message: types.Message, state: FSMContext) -> None:
    print(f"Received message from {message.from_user.id}: {message.text}")
    await state.clear()
    await message.reply(
        "Пожалуйста, выберите действие из контекстного меню:",
        reply_markup=get_main_keyboard()
    )