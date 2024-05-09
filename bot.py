#Пароль генератор бот

import random
import os
import string
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
logging.basicConfig(level=logging.INFO)

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

async def set_default_commands(dp):
    await bot.set_my_commands(
        [
            types.BotCommand('start' , 'Старт'),
            types.BotCommand('gen_password' , 'Генерація паролю')
        ]
    )

async def on_startup(dp):
    await set_default_commands(dp)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply("Привіт! Я зможу загенерувати пароль для тебе. Просто напиши команду /gen_password ")

PASSWORDCHOISE = types.InlineKeyboardMarkup() 
PASSWORDCHOISE.add(types.InlineKeyboardButton(text="Так", callback_data="yes")) 
PASSWORDCHOISE.add(types.InlineKeyboardButton(text="НІ", callback_data="no")) 


@dp.message_handler(commands= 'gen_password') 
async def generate_random_password( message_handler:types.Message, state: FSMContext): 
    password = gen_password() 
    await message_handler.answer(
f"Ваш пароль <code>{password}</code> Бажаєте перегенерувати?", 
parse_mode="html", 
reply_markup=PASSWORDCHOISE) 
def gen_password():
    length = 8
    chars = string.ascii_letters + string.digits + '!,@#%^&*()_-+=~`?/. '
    return ''.join(random.choice(chars) for _ in range(length))




@dp.callback_query_handler(lambda callback_query: callback_query.data in ["yes", "no"]) 
async def edit_password(callback_query: types.CallbackQuery, state: FSMContext): 
    if callback_query.data == "yes": 
        password = gen_password()
        await bot.edit_message_text( 
chat_id=callback_query.message.chat.id, 
message_id=callback_query.message.message_id, 
text=f"Ваш пароль<code>{password}</code> Бажаєте перегенерувати?", 
parse_mode="html", 
reply_markup=PASSWORDCHOISE) 
    else: 
        await bot.edit_message_reply_markup(
chat_id=callback_query.message.chat.id, 
message_id=callback_query.message.message_id, 
reply_markup= None )


        await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text="Дякую за користування !"
)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
