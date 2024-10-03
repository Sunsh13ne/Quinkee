from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Функция создания кнопок главного меню
async def menu_buttons():
    inline_button_help = InlineKeyboardButton(text='📖 Справка', callback_data='help')
    inline_button_searchgames = InlineKeyboardButton(text='🔎 Поиск игр', callback_data='searchgame')
    inline_button_trackedgames = InlineKeyboardButton(text='📀 Отслеживаемые игры', callback_data='trackedgames')
    inline_button_top = InlineKeyboardButton(text='🔥 Топ игр', callback_data='top')
    inline_button_history = InlineKeyboardButton(text='🕒 История поиска', callback_data='history')

    inline_menu = InlineKeyboardMarkup(inline_keyboard=[
        [inline_button_searchgames],
        [inline_button_trackedgames],
        [inline_button_top],
        [inline_button_help],
        [inline_button_history]
    ])
    return inline_menu