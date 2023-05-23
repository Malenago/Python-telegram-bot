from aiogram import Bot, Dispatcher, executor, types
import os, random



# webhook settings
WEBHOOK_HOST = 'https://your.domain'
WEBHOOK_PATH = '/path/to/api'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 3001


API_TOKEN = '...'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\n Я бот-котик. Отправь мне /cat, а я тебе обязательно отвечу!!!")


@dp.message_handler(commands=['cat'])
async def echo(message: types.Message):
    photo = open('cats/' + random.choice(os.listdir('cats')), 'rb')
    await bot.send_photo(message.chat.id, photo)



if __name__ == '__main__':
    executor.start_polling(dp)