from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from resources import keyboards as kb
from config import admin_ids, dp, bot
from aiogram.dispatcher.filters import IDFilter
from states import Table
import db

@dp.callback_query_handler(lambda c: c.data == 'cancel', IDFilter(admin_ids),  state = "*")
async def cancel_mailing_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(True)
    await callback_query.message.answer('Отменено')

@dp.message_handler(IDFilter(admin_ids), commands='admin')
async def start_admin_handler(msg: Message):
    await msg.answer('Привет, админ.', reply_markup=kb.reply_admin)

@dp.message_handler(lambda msg: msg.text == 'Прикрепить таблицу', IDFilter(admin_ids))
async def start_setting_table_handler(msg: Message):
    await msg.answer('Напиши id пользователя.')
    await Table.set_user_id.set()

@dp.message_handler(IDFilter(admin_ids), state = Table.set_user_id)
async def setting_uid_handler(msg: Message, state: FSMContext):
    try:
        data = db.get_user(msg.text)
    except Exception as e:
        print(e)
        await msg.answer('Неверный id, попробуйте снова')
        await state.reset_state()
    if not data:
        await msg.answer('Пользователь не найден. Попробуйте снова.')
        await state.reset_state()
    else:
        await state.update_data(user_id = msg.text)
        await state.set_state(Table.set_image)

@dp.message_handler(IDFilter(admin_ids), state = Table.set_image, content_types = ContentType.PHOTO)
async def setting_image_handler(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    u_id = state_data['user_id']
    db_data = db.get_images(
        user_id = u_id,
        title = 'chart'
    )
    file_info = await bot.get_file(msg.photo[-1].file_id)
    byte_photo = (await bot.download_file(file_info.file_path)).read()
    if not db_data:
        db.create_diary_image(
            user_id = u_id,
            title = 'chart',
            image = byte_photo
        )
    else:
        db.update_chart_image(
            user_id = u_id,
            image = byte_photo
        )
    await msg.answer('Таблица привязана!')

# start add contact
# @dp.message_handler(lambda msg: msg.text == 'Добавить контакт', IDFilter(admin_ids))
# async def add_contact_handler(msg: Message):
#     await msg.answer('Напиши ник', reply_markup = kb.inline_client_cancel)
#     await Friends.set_username.set()

# # setting username and user id
# @dp.message_handler(IDFilter(admin_ids), state=Friends.set_username)
# async def set_username_handler(msg: Message, state: FSMContext):
#     username = msg.text
#     await state.update_data(username=username)
#     await msg.answer('Напиши id пользователя')
#     await state.set_state(Friends.set_id)

# # finish add contact
# @dp.message_handler(IDFilter(admin_ids), state=Friends.set_id)
# async def set_description_handler(msg: Message, state: FSMContext):
#     try:
#         user_id = msg.text
#         state_data = await state.get_data()
#         create_user(user_id, state_data['username'])
#         await msg.answer('Готово, контакт добавлен!')
#         await state.finish()
#     except Exception as e:
#         print(e)
#         await state.reset_state(with_data = True)
#         await msg.answer('Что-то пошло не так, попробуйте снова')

# # start deleting contact
# @dp.message_handler(lambda msg: msg.text == 'Удалить контакт', IDFilter(admin_ids))
# async def start_deleting_handler(msg: Message):
#     try:
#         contacts = get_contacts()
#         markup = kb.create_location_markup(contacts, with_cancel = True)
#         await msg.answer(
#             text = 'Выберите контакт, который ходите удалить:',
#             reply_markup = markup
#         )
#         await Del_Friend.set_username.set()
#     except:
#         await msg.answer('Что-то пошло не так, попробуйте снова')

# # finish deleting contact
# @dp.callback_query_handler(IDFilter(admin_ids), state=Del_Friend.set_username)
# async def finish_deleting_handler(callback_query: types.CallbackQuery, state: FSMContext):
#     try:
#         delete_contact(callback_query.data.split('_')[1])
#         await callback_query.message.answer('Удаление завершено!')
#         await state.finish()
#     except Exception as e:
#         print(e)
#         await callback_query.message.answer('Что-то пошло не так, попробуйте снова')
#         await state.reset_state(with_data = True)

# @dp.callback_query_handler(lambda c: c.data.startswith('confirm'))
# async def confirmation_handler(callback_query: CallbackQuery):
#     await Sending_location.set_location.set()
#     username = callback_query.data.split('_')[1]
#     await dp.current_state().update_data(username = username)
#     # await set_state_location(dp.current_state(), username)
#     await callback_query.message.answer('Нажми кнопку "Поделиться"', reply_markup=kb.reply_send_location)

# # async def set_state_location(state: FSMContext, username: str):
# #     await state.update_data(username = username)

# @dp.message_handler(content_types = ContentType.LOCATION)
# async def send_handler(msg: Message):
#     bot_msg = await bot.send_location(
#         # chat_id = get_contactsId_by_name(state_data['username']),
#         latitude = msg.location.latitude,
#         longitude = msg.location.longitude,
#         live_period = msg.location.live_period
#     )
#     # await state.set_state(Sending_location.polling_location)
#     # await state.update_data(msg_id = bot_msg.message_id)
#     # await state.update_data(chat_id = bot_msg.chat.id)
#     await msg.answer('Локация отправлена!')

# @dp.edited_message_handler(content_types = ContentType.LOCATION,  state = Sending_location.polling_location)
# async def edit_location_handler(msg: Message, state: FSMContext):
#     print(msg)
#     state_data = await state.get_data()
#     if msg.location.live_period == None:
#         await bot.delete_message(
#             chat_id = state_data['chat_id'],
#             message_id = state_data['msg_id']
#         )
#         await state.finish()
#         return
#     await bot.edit_message_live_location(
#         latitude = msg.location.latitude,
#         longitude = msg.location.longitude,
#         chat_id = state_data['chat_id'],
#         message_id = state_data['msg_id'],
#         horizontal_accuracy = msg.location.horizontal_accuracy,
#         heading = msg.location.heading
#     )

# @dp.callback_query_handler(lambda c: c.data.startswith('conf_cancel'), state = "*")
# async def cancel_handler(callback_query: CallbackQuery):
#     await bot.send_message(get_contactsId_by_name(callback_query.data.split('_')[2]), '💼 Водила послал вас нахуй, всего доброго. 💼')