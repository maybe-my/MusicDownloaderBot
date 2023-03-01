from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_btn_add_to_channel = InlineKeyboardButton("Добавить в канал", callback_data='add_to_channel')
inline_add_to_channel = InlineKeyboardMarkup().add(inline_btn_add_to_channel)
