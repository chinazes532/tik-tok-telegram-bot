from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import admin_us


admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Спонсоры", callback_data='sponsors'),
        ],
        [
            InlineKeyboardButton(text="Рассылка", callback_data='mail'),
        ],
        [
            InlineKeyboardButton(text="Пользователи", callback_data='users'),
        ],
    ]
)

back_to_sponsors = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="↩️Вернуться назад", callback_data='sponsors'),
        ],
    ]
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="↩️Вернуться назад", callback_data='menu'),
        ],
    ]
)

feedback = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Связь с админом", url=f"https://t.me/{admin_us}"),
        ],
    ]
)
