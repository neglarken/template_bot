from aiogram import executor
from config import admin_ids, bot, level
import db
from multiprocessing import *
from client import dp
from admin import dp



async def on_startup(dp):
    db.create_db()

    if level != 'dev':
        for i in admin_ids:
            try:
                await bot.send_message(i, "Бот запущен")
            except:
                pass

async def on_shutdown(dp):
    await bot.close()
    if level != 'dev':
        for i in admin_ids:
            try:
                await bot.send_message(i, "Бот выключен")
            except:
                pass

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates = False)