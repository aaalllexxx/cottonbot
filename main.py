import asyncio
import base64

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile

from environment import Environment
import random

env = Environment(".env")

bot = Bot(env.token)
dp = Dispatcher(bot)


def create_image(b64):
    with open("temp/temp.jpg", "wb") as file:
        file.write(base64.urlsafe_b64decode(b64))


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привет, я бот, который поможет тебе выбрать товары с сайта магазина Cotton.\n"
                         "Напиши /help, чтобы узнать, что я могу.")


@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    await message.answer("/products - пять интересных продуктов с нашего сайта.\n"
                         "/brands - показать бренды.\n"
                         "/categories - показать категории.\n"
                         "/brand <название бренда> - показатьвсе продукты бренда.\n"
                         "/gender <male/female> - показать товары для мужчин или для женщин.\n"
                         "/category <название категории> - показать товары из определённой категории.")


@dp.message_handler(commands=["products"])
async def cmd_products(message: types.Message):
    resp = requests.get(env.base_url + "api/get")
    response = []
    if resp.status_code == 200:
        resp_json: list = resp.json()["response"]
        for i in range(5):
            choice = random.choice(list(resp_json))
            response.append(resp_json[choice])
            del resp_json[choice]
    for i in response:
        create_image(i["image_1"])
        image = InputFile("temp/temp.jpg")
        await bot.send_photo(message.chat.id, image, caption=f"{i['name']}\n\n{i['desc']}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
