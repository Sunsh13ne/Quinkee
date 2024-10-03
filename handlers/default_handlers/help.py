from loader import dp
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.inline.back_to_menu_button import back_to_menu_button


# Обработчик команды /help
@dp.message(Command('help'))
async def handle_help_command(message: Message, state: FSMContext):
    await send_help(message, state)

# Обработчик нажатия на кнопку "Справка"
@dp.callback_query(F.data == 'help')
async def handle_help_callback(callback_query: CallbackQuery, state: FSMContext):
    await send_help(callback_query, state)

# Обработчик команды /help и нажатия на кнопку "Справка"
async def send_help(message_or_callback: Message | CallbackQuery, state: FSMContext):
    await state.clear()

    help_text = (
        '📋 *Справка по боту*\n\n'
        '1️⃣ *Запуск бота*\n'
        'Команда /start — для начала работы с ботом.\n\n'
        
        '2️⃣ *Поиск игр*\n'
        'Вы можете найти игру и получить подробную информацию о ней, воспользовавшись:\n'
        '   • пунктом меню "Поиск игр"\n'
        '   • командой /searchgame.\n'
        'Каждую найденную игру можно добавить в "Отслеживаемые", '
        'чтобы получать уведомления об обновлениях или изменении цены.\n\n'
        
        '3️⃣ *Отслеживаемые игры*\n'
        'Для того чтобы увидеть список отслеживаемых игр и получить подробную информацию '
        'о каждой игре, воспользуйтесь:\n'
        '   • пунктом меню "Отслеживаемые игры"\n'
        '   • командой /trackedgames.\n\n'
        
        '4️⃣ *Топ игр*\n'
        'Для получения списка популярных игр в Steam, воспользуйтесь:\n'
        '   • пунктом меню "Топ игр"\n'
        '   • командой /top.\n\n'
        
        '5️⃣ *История поиска*\n'
        'Для получения сведений о просмотренных играх, воспользуйтесь:\n'
        '   • пунктом меню "История поиска"\n'
        '   • командой /history.\n'
        'Здесь вам нужно будет указать дату, за которую требуется история поиска.\n\n'

        '6️⃣ *Справка*\n'
        'Для ознакомления с функционалом бота, воспользуйтесь:\n'
        '   • пунктом меню "Справка"\n'
        '   • командой /help.\n\n'
        
        'Используйте эти команды и пункты меню для комфортной работы с ботом! 😊'
    )
    
    back_button = await back_to_menu_button()
    help_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])

    if isinstance(message_or_callback, Message):
        # Если вызвано командой /help
        await message_or_callback.answer(help_text, parse_mode='Markdown', reply_markup=help_keyboard)
    elif isinstance(message_or_callback, CallbackQuery):
        # Если вызвано из меню
        await message_or_callback.message.edit_text(help_text, parse_mode='Markdown', reply_markup=help_keyboard)
        await message_or_callback.answer()

