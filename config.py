import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import LabeledPrice
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get('TOKEN') #hehe nice
level = 'dev'

bot = Bot(token=token, parse_mode='HTML')
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)


admin_ids = [978086688]