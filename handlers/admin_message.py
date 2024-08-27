import logging

from aiogram import F, Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from filters.is_admin import AdminProtect

from states import Sms, ChangeLink, Sponsor

import keyboards.inline as ikb
import keyboards.builder as bkb

from database import *

admin = Router()

@admin.message(AdminProtect(), F.text == "Админ-панель")
async def admin_panel(message: Message):
    await message.answer(f"Вы вошли в админ-панель!\n"
                         f"Выберите действие",
                         reply_markup=ikb.admin_panel)

@admin.callback_query(F.data == "mail")
async def mail(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите сообщение для рассылки:",
                                  reply_markup=ikb.back)
    await state.set_state(Sms.text)

@admin.message(Sms.text)
async def send_text(message: Message, state: FSMContext):
    await message.answer("Рассылка запущена!")
    users = await get_users()

    for user in users:
        try:
            await message.send_copy(chat_id=user[0])

        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения пользователю {user[0]}: {str(e)}")
            if "Telegram server says - Forbidden: bot was blocked by the user" in str(e):
                await delete_user(user[0])

    count = await user_count()
    await message.answer(f"Рассылка завершена!\n\n"
                         f"{count} пользователей получили сообщение",
                         reply_markup=ikb.admin_panel)
    await state.clear()
@admin.callback_query(F.data == "users")
async def users(callback: CallbackQuery):
    users = await get_users()
    user_list = ""
    for user in users:
        user_id, username = user
        if username != 'None':
            user_list += f"{user_id} - @{username}\n"
        else:
            user_list += f"{user_id}\n"
    try:
        await callback.message.edit_text(f'Все пользователи: \n{user_list}',
                                         reply_markup=ikb.back)
    except TelegramBadRequest:
        await callback.message.answer(f'Все пользователи: \n{user_list}',
                                      reply_markup=ikb.back)
@admin.callback_query(F.data == "sponsors")
async def sponsors(callback: CallbackQuery):
    await callback.message.answer("Все спосносры:",
                                  reply_markup=await bkb.get_sponsors_cb())
@admin.callback_query(F.data == "add_sponsor")
async def add_sponsor(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите имя спонсора:",
                                  reply_markup=ikb.back_to_sponsors)
    await state.set_state(Sponsor.name)

@admin.message(Sponsor.name)
async def sponsor_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Sponsor.group_id)
    await message.reply('Введите Group_id или Chat_id спонсора\n\n\n'
                        'взять ID группового чата можно в боте @LeadConverterToolkitBot\n'
                        'взять ID Канала: https://telegramid.lavrynenko.com',
                        reply_markup=ikb.back_to_sponsors)

@admin.message(Sponsor.group_id)
async def sponsor_group_id(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(group_id=message.text)
        await state.set_state(Sponsor.link)
        await message.reply('Введите ссылку на спонсора без @ \n\n❌@sponsor\n✅sponsor',
                            reply_markup=ikb.back_to_sponsors)
    else:
        await message.reply('Некорректный Group_id, введите цифры',
                            reply_markup=ikb.back_to_sponsors)
@admin.message(Sponsor.link)
async def sponsor_link(message: Message, state: FSMContext):
    if '@' in message.text:
        await message.reply('Некорректная ссылка, введите ссылку без @',
                            reply_markup=ikb.back_to_sponsors)
    else:
        await state.update_data(link=message.text)
        data = await state.get_data()
        name = data.get('name')
        group_id = data.get('group_id')
        link = data.get('link')
        await insert_sponsor(name, group_id, link)
        await message.reply('Спонсор добавлен',
                            reply_markup=await bkb.get_sponsors_cb())
        await state.clear()
@admin.callback_query(F.data.startswith('sponsor_'))
async def sponsor_options_handler(callback: CallbackQuery):
    sponsor_id = callback.data.split("_")[1]
    sponsor = await get_sponsor(sponsor_id)
    text = (
            f"✨ Выберите действие для спонсора ✨\n\n"
            f"👤 Имя Спонсора: {sponsor[1]}\n"
            f"🔗 Ссылка: @{sponsor[3]}\n"
            f"💬 Group ID: {sponsor[2]}\n"
        )
    try:
        await callback.message.edit_text(text=text,
                                         reply_markup=await bkb.sponsor_options(id=sponsor_id))
    except TelegramBadRequest:
        await callback.message.answer(text=text,
                                      reply_markup=await bkb.sponsor_options(id=sponsor_id))

@admin.callback_query(F.data.startswith('delete_'))
async def delete_sponsor_func(callback: CallbackQuery):
    await delete_sponsor(callback.data.split("_")[1])
    await callback.message.edit_text('Спонсор удален',
                                     reply_markup=await bkb.get_sponsors_cb())

@admin.callback_query(F.data.startswith('edit_sponsor_link_'))
async def edit_sponsor(callback: CallbackQuery, state: FSMContext):
    sponsor_id = callback.data.split('_')[3]
    await state.update_data(sponsor_id=sponsor_id)
    await state.set_state(ChangeLink.link_change)
    await callback.message.edit_text('Введите ссылку на спонсора без @ \n\n❌@sponsor\n✅sponsor',
                                     reply_markup=ikb.back_to_sponsors)

@admin.message(ChangeLink.link_change)
async def edit_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    sponsor_id = data.get('sponsor_id')
    link = data.get('link')
    await update_sponsor_link(sponsor_id, link)

    await message.answer(f'Ссылка для спонсора {sponsor_id} изменена',
                         reply_markup=await bkb.get_sponsors_cb())
    await state.clear()

@admin.callback_query(F.data.startswith("edit_sponsor_group_id_"))
async def edit_group_id(callback: CallbackQuery, state: FSMContext):
    sponsor_id = callback.data.split('_')[4]
    await state.update_data(sponsor_id=sponsor_id)
    await state.set_state(ChangeLink.group_sponsor_id)
    await callback.message.edit_text('Введите Group_id или Chat_id спонсора\n\n\n'
                                     'взять ID группового чата: @LeadConverterToolkitBot\n'
                                     'взять ID Канала: https://telegramid.lavrynenko.com',
                                     reply_markup=ikb.back_to_sponsors)

@admin.message(ChangeLink.group_sponsor_id)
async def edit_group_id(message:Message, state: FSMContext):
    await state.update_data(group_id=message.text)
    data = await state.get_data()
    sponsor_id = data.get('sponsor_id')
    group_id = data.get('group_id')
    await update_sponsor_group_id(sponsor_id, group_id)

    await message.answer(f'Группа для спонсора {sponsor_id} изменена',
                         reply_markup=await bkb.get_sponsors_cb())
    await state.clear()

@admin.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Главное меню:",
                                  reply_markup=ikb.admin_panel)






