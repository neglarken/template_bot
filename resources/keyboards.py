from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonRequestUser

# Client
btn_add_friend = KeyboardButton(
    text = 'Добавить друга',
    request_user = KeyboardButtonRequestUser(1, False)
)
btn_delete_friend = KeyboardButton('Удалить друга')
btn_get_location = KeyboardButton('Получить геолокацию')
btn_friend_invites = KeyboardButton('Заявки в друзья')
btn_help = KeyboardButton('Помощь')
get_location = ReplyKeyboardMarkup(resize_keyboard=True).add(
    btn_get_location,
    btn_add_friend,
    btn_delete_friend,
    btn_friend_invites,
    btn_help
)

inline_btn_client_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
inline_client_cancel = InlineKeyboardMarkup().add(inline_btn_client_cancel)

def create_request_markup(user_name: str, user_id: int, sub_id: int):
    inline_btn_ok = InlineKeyboardButton('Да!', callback_data = f'request_{user_name}_{user_id}_{sub_id}')
    return InlineKeyboardMarkup().add(inline_btn_ok, inline_btn_client_cancel)

def create_invite_markup(user_id: int, username: str):
    inline_accept_invite = InlineKeyboardButton('Принять', callback_data = f'accept_{user_id}_{username}')
    inline_deny_invite = InlineKeyboardButton('Отклонить', callback_data = f'deny_{user_id}')
    return InlineKeyboardMarkup().add(inline_accept_invite, inline_deny_invite)

def create_location_markup(contacts_array: list, with_cancel = False):
    inline_contacts = InlineKeyboardMarkup(row_width=1)
    for contact in contacts_array:
        inline_btn_contact = InlineKeyboardButton(contact[1], callback_data = f'contact_{contact[0]}')
        inline_contacts.add(inline_btn_contact)
    if with_cancel:
        inline_contacts.add(inline_btn_client_cancel)
    return inline_contacts

# Admin
add_table = KeyboardButton('Прикрепить таблицу')

reply_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(
    add_table
)

def create_confirmation_reply(username):
    inline_confirm = InlineKeyboardButton('Подтвердить', callback_data=f'confirm_{username}')
    inline_admin_cancel = InlineKeyboardButton('Отказать', callback_data=f'conf_cancel_{username}')

    reply_confirmation = InlineKeyboardMarkup(row_width=1).add(
        inline_confirm,
        inline_admin_cancel
    )
    return reply_confirmation

btn_send_location = KeyboardButton('Поделиться', request_location = True)
reply_send_location = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_send_location)