from database.models import User
from loader import dp
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.inline.menu_buttons import menu_buttons
from loader import bot

# Обработчик команды /start
@dp.message(Command('start'))
async def send_welcome(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    user, created = User.get_or_create(user_id=user_id, defaults={'username': username})
    # Выводим приветствие, если новый пользователь
    if created:
        bot_info = await bot.get_me()
        bot_name = bot_info.first_name
        await message.answer(f'Здравствуйте, *{first_name}*! Добро пожаловать!\n'
                             f'Меня зовут 👻*{bot_name}*. Я помогу найти нужные вам игры, '
                             'дам вам подробную информацию о них, а также оповещу вас '
                             'об обновлениях и событиях связанных с ними, включая изменение цен. '
                             'Вы также сможете узнать какие игры сейчас популярны в Steam.\n'
                             'Воспользуйтесь кнопкой *"Справка"* в меню или командой /help, '
                             'чтобы получить больше информации о возможностях и поддерживаемых командах.',
                             parse_mode="Markdown")

    menu_keyboard = await menu_buttons()
    await message.answer("\nㅤ\n ──────   *Главное меню*   ────── \nㅤ",
                         reply_markup=menu_keyboard,
                         parse_mode="Markdown")