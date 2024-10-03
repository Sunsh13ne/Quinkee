from database.models import User, UserTrackedGame

# Функция проверки отслеживания игры пользователем
async def check_if_tracked_game(user_id: int, appid: int) -> bool:
    user = User.get_or_none(User.user_id == user_id)
    if user:
        return UserTrackedGame.select().where(
            UserTrackedGame.user == user,
            UserTrackedGame.tracked_game == appid
        ).exists()
    return False