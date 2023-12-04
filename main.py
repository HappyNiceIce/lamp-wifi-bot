import asyncio
from aiogram import types, Bot, executor
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ContentType, InputMediaPhoto, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import pars
from config import bot_token, admin_id


storage = MemoryStorage()
bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

async def on_startup(dispatcher):
    try:
        await bot.send_message(chat_id=admin_id, text="Bot started")
    except:
        pass

#
class color(StatesGroup):
    r = State()
    g = State()
    b = State()
class brightness(StatesGroup):
    brightness = State()


@dp.message_handler(commands=["start"], chat_id=admin_id)
async def question(message: types.Message):
    klava = InlineKeyboardMarkup(row_width=1)
    butt_1 = InlineKeyboardButton(text="Веселка", callback_data="raindow")
    butt_2 = InlineKeyboardButton(text="Переливання", callback_data="transfusion")
    butt_3 = InlineKeyboardButton(text="Яскравість", callback_data="brightness")
    butt_4 = InlineKeyboardButton(text="Кольор", callback_data="rgb")
    klava.add(butt_1, butt_2, butt_3, butt_4)
    await message.answer(text="Що ти хочеш змінити?", reply_markup=klava)

@dp.callback_query_handler()
async def quere_color(callback: types.CallbackQuery):
    if callback.data == "raindow":
        pars.rainbow()

    if callback.data == "transfusion":
        pars.transfusion()

    elif callback.data == "brightness":
        await callback.message.answer(text="Введи яскравість від 0 до 255: ")
        await brightness.brightness.set()
        @dp.message_handler(state=brightness.brightness)
        async def red_brightness(message: types.Message, state: FSMContext):
            try:
                brightness_value = int(message.text)
                if 0 <= brightness_value <= 255:
                    # Вы можете использовать полученное значение яркости здесь
                    await message.answer(f"Ви ввели яскравість: {str(brightness_value)}")
                    pars.brightness(value=str(brightness_value))
                    await state.finish()
                else:
                    await message.answer("Яскравість повинна бути в межах від 0 до 255. Спробуйте ще раз.")
            except ValueError:
                await message.answer("Будь ласка, введіть ціле число.")

    elif callback.data == "rgb":
        await callback.message.answer(text="Введи red від 0 до 255: ")
        await color.r.set()

        @dp.message_handler(state=color.r)
        async def red(message: types.Message, state: FSMContext):

            try:
                red_value = int(message.text)
                if 0 <= red_value <= 255:
                # Вы можете использовать полученное значение яркости здесь
                    await message.answer(f"Ви ввели червоний: {str(red_value)}")
                    async with state.proxy() as data:
                        data["red"] = red_value
                    await message.answer(text="Введи green від 0 до 255: ")
                    await color.g.set()
                else:
                    await message.answer("Колір має бути в межах від 0 до 255. Спробуйте знову.")
            except ValueError:
                    await message.answer("Будь ласка, введіть ціле число.")

        @dp.message_handler(state=color.g)
        async def green(message: types.Message, state: FSMContext):
            try:
                green_value = int(message.text)
                if 0 <= green_value <= 255:
                    # Вы можете использовать полученное значение яркости здесь
                    await message.answer(f"Ви ввели зелений: {str(green_value)}")
                    async with state.proxy() as data:
                        data["green"] = message.text
                    await message.answer(text="Введи blue від 0 до 255: ")
                    await color.b.set()
                else:
                    await message.answer("Колір має бути в межах від 0 до 255. Спробуйте знову.")
            except ValueError:
                await message.answer("Будь ласка, введіть ціле число.")


        @dp.message_handler(state=color.b)
        async def blue(message: types.Message, state: FSMContext):
            try:


                blue_value = int(message.text)
                if 0 <= blue_value <= 255:
                    # Вы можете использовать полученное значение яркости здесь
                    await message.answer(f"Ви ввели синій: {str(blue_value)}")
                    async with state.proxy() as data:
                        data["blue"] = message.text
                    await state.finish()
                    pars.rgb(r=data["red"], g=data["green"], b=data["blue"])
                else:
                    await message.answer("Колір має бути в межах від 0 до 255. Спробуйте знову.")
            except ValueError:
                await message.answer("Будь ласка, введіть ціле число.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
