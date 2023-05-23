import os
from aiogram import Bot, Dispatcher, types, executor
import pytesseract
from PIL import Image
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


WEBHOOK_HOST = 'https://your.domain'
WEBHOOK_PATH = '/path/to/api'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001


API_TOKEN = '...'


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)


class UserState(StatesGroup):
    lang = State()
    photo=State()


def photo_text(path,lang):
    return pytesseract.image_to_string(Image.open(path), lang=lang, config=r'--oem 3 --psm 6')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Русский 🇷🇺", "Английский 🇬🇧"]
    keyboard.add(*buttons)

    await message.answer("Привет! ☺️\n"
                        "Я помогу тебе распознать текст с картинки, \n"
                        "выбери язык текста на картинке:",
                        reply_markup=keyboard)

    await UserState.lang.set()


@dp.message_handler(state=UserState.lang)
async def send_lang(message: types.Message, state: FSMContext):
    await state.update_data(lang=message.text)

    await message.answer("Супер! 💓️\n"
                        f"Выбранный язык: {message.text} \n"
                        "Теперь отправьте картинку",
                        reply_markup=types.ReplyKeyboardRemove())

    await UserState.photo.set()

@dp.message_handler(content_types=[types.ContentType.PHOTO],state=UserState.photo)
async def process_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1])
    data = await state.get_data()

    lang = ''
    text = ''

    if "Русский 🇷🇺" in {data['lang']}:
        lang="rus"
    else:
        lang="eng"

    await message.photo[-1].download(destination="somedir/")

    for file in os.listdir('somedir/photos/'):
        path='somedir/photos/'+str(file)

        text+=(str(photo_text(path,lang))+'\n')
        os.remove(path)

        if text!='':
            await message.answer(text)
        else:
            await message.answer(f"Упс...Фото без текста")

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)


