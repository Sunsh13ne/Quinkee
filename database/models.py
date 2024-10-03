from datetime import datetime
import time
from peewee import Model, CharField, IntegerField, ForeignKeyField, SqliteDatabase, DateTimeField
from config_data.config import DB_PATH

# Инициализация базы данных
db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db

# Модель пользователя
class User(BaseModel):
    user_id = IntegerField(unique=True, primary_key=True)
    username = CharField(null=True)

# Модель отслеживаемых игр
class TrackedGame(BaseModel):
    appid = IntegerField(unique=True, primary_key=True)
    title = CharField()
    last_updated_at = IntegerField(default=int(time.time()))
    price = IntegerField(null=True, default=None)

# Промежуточная модель для связи пользователей и отслеживаемых игр
class UserTrackedGame(BaseModel):
    user = ForeignKeyField(User, backref='tracked_games')
    tracked_game = ForeignKeyField(TrackedGame, backref='users')
    created_at = IntegerField(default=int(time.time()))

# Модель для хранения истории запросов
class SearchHistory(BaseModel):
    user = ForeignKeyField(User, backref='search_history')
    game = ForeignKeyField(TrackedGame, backref='search_history')
    searched_at = DateTimeField(default=datetime.now)

# Функция создания таблиц
def create_models():
    db.create_tables(BaseModel.__subclasses__())
