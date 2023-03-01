import os
import validators
import datetime
import config
from dispatcher import dp
from aiogram.types import ContentType
from dispatcher import bot
from aiogram import types

from keyboards.keyboards import inline_add_to_channel
from scripts.shazam import shazam_voice
from scripts.downloadMp3 import download

user_data = {}


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Знакомство с ботом `/start`
    """

    global greet
    opts = {"hey": ('Привет', 'Здравствуйте', 'Доброе утро', 'Добрый день', 'Добрый вечер', 'Доброй ночи')}

    now = datetime.datetime.now()
    if 4 < now.hour <= 12:
        greet = opts["hey"][2]
    if 12 < now.hour <= 16:
        greet = opts["hey"][3]
    if 16 < now.hour <= 24:
        greet = opts["hey"][4]
    if 0 <= now.hour <= 4:
        greet = opts["hey"][5]

    await message.answer(f"{greet}, Хелоу 🔍")


@dp.message_handler(content_types=[ContentType.TEXT])
async def send_welcome(message: types.Message):
    # Скачивание и добавление музыки в канал
    if validators.domain(message.text) or validators.url(message.text):
        mess = await message.reply("⚠️ Скачиваю...")
        try:
            music = download(message.text)
            with open(music['path'], mode="rb") as file:
                binary_content = file.read()
            await mess.delete()
            await message.answer_audio(binary_content, title=music['name'], reply_markup=inline_add_to_channel)
            user_data[message.from_user.id] = music
        except:
            await mess.edit_text(f"❌ Не нашел здесь музыку")
    else:
        await message.reply("Что?")


@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: types.Message):
    voice = await bot.get_file(message.voice.file_id)
    sound = shazam_voice(voice.file_path)

    if sound['result'] is None:
        await message.reply(f"{message.chat.first_name.title()}, запиши еще раз и по дольше.")
    else:
        s = sound['result']['lyrics']['media']
        await message.answer(s.stri)
        await message.answer(
            f""" \
            {sound['result']['title'].strip()} by #{sound['result']['artist'].replace(' ', '_').strip().replace(',', '')}
            """)


# Обработка кнопоки
@dp.callback_query_handler(lambda c: c.data == 'add_to_channel')
async def process_callback_add_to_channel(callback_query: types.CallbackQuery):
    if user_data[callback_query.from_user.id]:
        music = user_data[callback_query.from_user.id]
        await bot.answer_callback_query(
            callback_query.id,
            text=f"✅ {music['name']} добавлено", show_alert=True)
        with open(music['path'], mode="rb") as file:
            binary_content = file.read()

        await bot.send_audio(chat_id=config.CHANNEL_ID, audio=binary_content,
                             title=music['name'])
        os.remove(music['path'])

        user_data[callback_query.from_user.id] = ''
    else:
        await bot.answer_callback_query(
            callback_query.id,
            text='❌ Уже добавлено в канал', show_alert=True)
