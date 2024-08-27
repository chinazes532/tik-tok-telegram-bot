import re

from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from filters.is_admin import AdminProtect
from filters.download import download
from filters.is_subscribe import subscription_check, subscription_check_cb

from database import insert_user

import keyboards.reply as rkb
import keyboards.inline as ikb
import keyboards.builder as bkb

from config import admin_us

user = Router()

@user.message(CommandStart())
async def start_command(message: Message):
    admin = AdminProtect()
    if not await admin(message):  # Добавляем await здесь
        await message.answer(f"Привет! Чтобы скачать видео, просто отправь ссылку на видео TikTok.\n"
                             f"Реклама/Добавление спонсоров - @{admin_us}",
                             reply_markup=ikb.feedback)
        await insert_user(message.from_user.id, message.from_user.username)
    else:
        await message.answer(f"Привет! Чтобы скачать видео, просто отправь ссылку на видео TikTok.\n"
                             f"Реклама/Добавление спонсоров - @{admin_us}",
                             reply_markup=ikb.feedback)
        await insert_user(message.from_user.id, message.from_user.username)
        await message.answer(f"Вы успешно авторизовались как администратор!",
                             reply_markup=rkb.admin_menu)


@user.message()
async def download_video(message: Message, bot):
    if not await subscription_check(message, bot):
        return  # Exit if the user is not subscribed

    # Проверка на корректность ссылки
    if re.match(r'https://[a-zA-Z]+\.tiktok\.com/', message.text):
        m = await message.reply('Ожидайте..')
        video_url = download(message.text)
        if video_url:
            await bot.delete_message(message.chat.id, m.message_id)
            await message.answer_video(video_url,
                                       caption='Спасибо, что пользуетесь нашим ботом! 🙏')
        else:
            await bot.delete_message(message.chat.id, m.message_id)
            await message.reply('Произошла ошибка при скачивании видео.')
    else:
        await message.reply('Ссылка не найдена. Пожалуйста, введите корректную ссылку на TikTok.')

@user.callback_query(F.data == 'check_subscription')
async def check_subscription(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    if not await subscription_check_cb(callback, bot):
        return  # Exit if the user is not subscribed

    await callback.message.answer('Спасибо за подписку!\n'
                                  'Теперь вам доступен полный функционал бота 🎉')








