from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Админ-панель"),
        ],
    ],
    resize_keyboard=True
)