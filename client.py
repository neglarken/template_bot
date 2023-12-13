from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from config import bot, dp
import db
from aiogram.types import ContentType, InputFile
from resources import texts
from resources import keyboards as kb
from states import MyStates

@dp.callback_query_handler(lambda c: c.data == 'cancel',  state = "*")
async def cancel_mailing_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.reset_state(True)
    await callback_query.message.answer('Отменено')

# start bot message
@dp.message_handler(commands=['start'])
async def start_handler(msg: Message):
    db.create_user(
        id = msg.from_user.id,
        name = msg.from_user.username
    )
    await msg.answer('Привет!')

@dp.message_handler(state = MyStates.set_first)
async def state_handler(msg: Message, state: FSMContext):
    pass

@dp.message_handler(lambda msg: msg.text == 'text')
async def msg_handler(msg: Message):
    pass

@dp.callback_query_handler(lambda c: c.data.startswith("start"))
async def cb_query_handler(callback_query: CallbackQuery):
    pass

@dp.edited_message_handler(content_types = ContentType.LOCATION)
async def content_type_handler(msg: Message):
    pass
