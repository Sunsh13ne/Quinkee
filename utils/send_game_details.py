from aiogram.types import Message, InlineKeyboardMarkup
from api.api_requests import fetch_game_details
from keyboards.inline.game_following_buttons import game_following_buttons
from keyboards.inline.back_to_menu_button import back_to_menu_button
from utils.check_if_tracked_game import check_if_tracked_game
from aiogram.fsm.context import FSMContext
from database.save_search_result import save_search_result

# Функция отправки детализации игры
async def send_game_details(message: Message,
                            state: FSMContext,
                            user_id: int,
                            game: dict,
                            previous_message: Message = None):
    game_appid = game['appid']
    game_name = game['name']
    game_details = await fetch_game_details(game_appid)
    steam_link = f'https://store.steampowered.com/app/{game_appid}/'

    # Проверка, отслеживается ли игра
    tracked_game = await check_if_tracked_game(user_id, game_appid)

    following_buttons = game_following_buttons(steam_link, tracked_game, game_appid)
    back_button = await back_to_menu_button()

    keyboard = InlineKeyboardMarkup(inline_keyboard=following_buttons.inline_keyboard + [[back_button]])

    if game_details:
        # Форматируем информацию для отправки
        name = game_details.get('name')
        genres = ', '.join([genre['description'] for genre in game_details.get('genres', [])])
        is_free = game_details.get('is_free',  False)
        price_overview = game_details.get('price_overview', {})
        price = 'Бесплатная' if is_free else price_overview.get('final_formatted', 'Неизвестно')
        description = game_details.get('short_description')
        release_date = game_details.get('release_date', {}).get('date', 'Неизвестно')
        header_image = game_details.get('header_image')
        
        # Проверка и извлечение разработчиков и издателей
        developers = game_details.get('developers', [])
        publishers = game_details.get('publishers', [])
        developer = ', '.join(developers)
        publisher = ', '.join(publishers)
        rating = game_details.get('metacritic', {}).get('score', 'Нет данных')

        response_message = (
            f'*Название:* {name}\n'
            f'*Жанры:* {genres}\n'
            f'*Цена:* {price}\n'
            f'*Описание:* {description}\n'
            f'*Дата выхода:* {release_date}\n'
            f'*Разработчик:* {developer}\n'
            f'*Издатель:* {publisher}\n'
            f'*Рейтинг Metacritic:* {rating}\n'
        )

        chosen_game_data = {
            'appid': game_appid,
            'name': name,
            'price': price
        }

        await save_search_result(callback=message,
                                 user_id=user_id,
                                 game_appid=game_appid,
                                 name=name,
                                 price=price)

        await message.answer_photo(
            photo=header_image, 
            caption=response_message, 
            reply_markup=keyboard, 
            parse_mode='Markdown')
        if previous_message:
            await previous_message.delete()
        await state.update_data(chosen_game_data=chosen_game_data)
    else:
        if previous_message:
            await previous_message.edit_text(
                f'Подробная информация об игре {game["name"]} не найдена.'
                '\nВозможно, она не доступна в Вашем регионе.',
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        else:
            await message.answer(
                f'Подробная информация об игре {game["name"]} не найдена.'
                '\nВозможно, она не доступна в Вашем регионе.',
                reply_markup=keyboard,
                parse_mode='Markdown'
            )

        chosen_game_data = {
            'appid': game_appid,
            'name': game_name,
            'price': 'Неизвестно'
        }
        await save_search_result(callback=message,
                                 user_id=user_id,
                                 game_appid=game_appid,
                                 name=game_name,
                                 price='Неизвестно')
        await state.update_data(chosen_game_data=chosen_game_data)
