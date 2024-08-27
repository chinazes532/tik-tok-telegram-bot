from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from database import get_sponsors

import keyboards.builder as bkb

async def is_subscribed(user_id, bot):
    sponsors = await get_sponsors()
    print("Sponsorship groups:", sponsors)

    for sponsor in sponsors:
        print(f"Checking membership for user {user_id} in group -{sponsor[2]}")
        try:
            member = await bot.get_chat_member(f'-{sponsor[2]}', user_id)
            print(f"Member status: {member.status}")
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except TelegramBadRequest as e:
            print(f"Error fetching chat member for group_id -{sponsor[2]}: {e}")
            continue

    return True

async def subscription_check(message: Message, bot):
    if not await is_subscribed(message.from_user.id, bot):
        await message.reply("Вы должны подписаться на наши группы, чтобы использовать этого бота.",
                            reply_markup=await bkb.subscribe())
        return False
    return True

async def is_subscribed_cb(user_id, bot):
    sponsors = await get_sponsors()
    print("Sponsorship groups:", sponsors)

    for sponsor in sponsors:
        print(f"Checking membership for user {user_id} in group -{sponsor[2]}")
        try:
            member = await bot.get_chat_member(f'-{sponsor[2]}', user_id)
            print(f"Member status: {member.status}")
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except TelegramBadRequest as e:
            print(f"Error fetching chat member for group_id -{sponsor[2]}: {e}")
            continue

    return True

async def subscription_check_cb(callback: CallbackQuery, bot):
    user_id = callback.from_user.id
    if not await is_subscribed_cb(user_id, bot):
        await callback.message.answer("Вы должны подписаться на наши группы, чтобы использовать этого бота.",
                                      reply_markup=await bkb.subscribe())
        return False
    return True

