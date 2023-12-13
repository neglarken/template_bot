from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from resources import keyboards as kb
from config import admin_ids, dp
from aiogram.dispatcher.filters import IDFilter

@dp.callback_query_handler(lambda c: c.data == 'cancel', IDFilter(admin_ids),  state = "*")
async def cancel_mailing_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(True)
    await callback_query.message.answer('Отменено')

@dp.message_handler(IDFilter(admin_ids), commands='admin')
async def start_admin_handler(msg: Message):
    await msg.answer('Привет, админ.', reply_markup=kb.reply_admin)

@dp.message_handler(lambda msg: msg.text == 'text', IDFilter(admin_ids))
async def add_contact_handler(msg: Message):
    pass