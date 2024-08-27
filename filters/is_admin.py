from aiogram.types import Message
from aiogram.filters import Filter

from config import ADMINS

# Фильтр на админку
class AdminProtect(Filter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins