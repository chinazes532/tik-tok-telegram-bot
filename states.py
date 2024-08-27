from aiogram.fsm.state import State, StatesGroup

# Сообщение для рассылки
class Sms(StatesGroup):
    text = State()

# Добавление спонсора для обязательной подписки
class Sponsor(StatesGroup):
    name = State()
    group_id = State()
    link = State()

# Редакирование спонсора
class ChangeLink(StatesGroup):
    sponsor_id = State()
    link_change = State()
    group_sponsor_id = State()