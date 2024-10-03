from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Функция создания навигации по списку игр
def get_pagination_buttons(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    buttons = []
    if total_pages != 1:
        if current_page == 1:
            buttons.append(InlineKeyboardButton(text="🚫", callback_data="current_page"))
            buttons.append(InlineKeyboardButton(text="🚫", callback_data="current_page"))
        if current_page > 1:
            buttons.append(InlineKeyboardButton(text="<< 1", callback_data="page_1"))
            buttons.append(InlineKeyboardButton(text=f"< {current_page - 1}", callback_data=f"page_{current_page - 1}"))

        # Кнопка с текущей страницей
        buttons.append(InlineKeyboardButton(text=f"-{current_page}-", callback_data="current_page"))
        
        if current_page < total_pages:
            buttons.append(InlineKeyboardButton(text=f"{current_page + 1} >", callback_data=f"page_{current_page + 1}"))
            buttons.append(InlineKeyboardButton(text=f"{total_pages} >>", callback_data=f"page_{total_pages}"))
        if current_page == total_pages:
            buttons.append(InlineKeyboardButton(text="🚫", callback_data="current_page"))
            buttons.append(InlineKeyboardButton(text="🚫", callback_data="current_page"))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return keyboard