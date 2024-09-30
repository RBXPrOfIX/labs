import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = '6517126548:AAFE0CGGktLTk4GxtOOS37xAMr9kyRl4IOg'

UNSPLASH_API_KEY = 'xtaOB5OOBZKYoMTMEoNtvGIEFve6ykphyublWSjbgz4'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который отправляет изображения по вашему запросу. Просто напишите мне что-нибудь!")


@dp.message_handler()
async def send_image(message: types.Message):
    query = message.text
    url = f'https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_API_KEY}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['urls']['regular']
                await message.reply_photo(photo=image_url)
            else:
                await message.reply("Извините, не удалось найти изображение по вашему запросу.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)