
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import pandas as pd

API_TOKEN = '7812679876:AAHhtr7nJNnU11FkJhrR7bAgwQUExQs6HR4'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    url = State()
    login = State()
    password = State()
    pages = State()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await Form.url.set()
    await message.reply("Введіть посилання на сторінку для парсингу:")

@dp.message_handler(state=Form.url)
async def process_url(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await Form.next()
    await message.reply("Введіть логін:")

@dp.message_handler(state=Form.login)
async def process_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await Form.next()
    await message.reply("Введіть пароль:")

@dp.message_handler(state=Form.password)
async def process_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await Form.next()
    await message.reply("Скільки сторінок потрібно обійти?")

@dp.message_handler(state=Form.pages)
async def process_pages(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    pages = int(message.text)
    await state.update_data(pages=pages)

    await message.reply("Парсинг запущено... Зачекайте.")

    excel_path = run_scraper(user_data['url'], user_data['login'], user_data['password'], pages)

    await message.reply_document(InputFile(excel_path))
    await state.finish()

def run_scraper(url, login, password, pages):
    df = pd.DataFrame([['Зразок результату 1'], ['Зразок результату 2']], columns=['Результат'])
    path = "result.xlsx"
    df.to_excel(path, index=False)
    return path

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
