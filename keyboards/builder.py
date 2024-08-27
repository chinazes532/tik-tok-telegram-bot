from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import get_sponsors, get_sponsor

async def get_sponsors_cb():
    sponsors = await get_sponsors()
    kb = InlineKeyboardBuilder()

    for sponsor in sponsors:
        kb.row(InlineKeyboardButton(text=f'{sponsor[1]}', callback_data=f'sponsor_{sponsor[0]}'))
    kb.row(InlineKeyboardButton(text='➕Добавить спонсора', callback_data='add_sponsor'))
    kb.row(InlineKeyboardButton(text='↩️Вернуться назад', callback_data='menu'))

    return kb.as_markup()

async def sponsor_options(id):
    sponsor = await get_sponsor(id)
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='👀Изменить Chat_Id или Group_Id', callback_data=f'edit_sponsor_group_id_{sponsor[0]}'))
    kb.row(InlineKeyboardButton(text='🔗Изменить ссылку', callback_data=f'edit_sponsor_link_{sponsor[0]}'))
    kb.row(InlineKeyboardButton(text='🗑Удалить спонсора', callback_data=f'delete_{sponsor[0]}'))

    kb.row(InlineKeyboardButton(text='↩️Вернуться назад', callback_data='sponsors'))

    return kb.as_markup()

async def subscribe():
    sponsors = await get_sponsors()
    kb = InlineKeyboardBuilder()

    for sponsor in sponsors:
        kb.row(InlineKeyboardButton(text=f'{sponsor[3]}', url=f'https://t.me/{sponsor[3]}'))
    kb.row(InlineKeyboardButton(text='✅Готово', callback_data='check_subscription'))

    return kb.as_markup()


