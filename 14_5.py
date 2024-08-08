from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_fuctions import *


api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
button2 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
kb.add(button1)
kb.add(button2)

registr_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Регистрация')]
    ]
)

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Купить'),
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Рассчитать')
        ]
    ], resize_keyboard=True
)

catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Рroduct3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ], resize_keyboard=True
)


class RegistrationState(StatesGroup):
    username = States()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит): ', reply_markup=registr_kb)
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    i_n_c = is_included(message.text)
    if i_n_c is True:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой емаил: ')
        await UserState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст: ')
    await UserState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    users_data = await state.get_data()
    add_user(username=users_data["username"], email=users_data["email"], age=users_data["age"])
    await state.finish()
    await message.answer("Регистрация прошла успешно")


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Введите команду /start, чтобы начать общение', reply_markup = start_kb)

@dp.message_handler(text = 'Информация')
async def info(message):
    await message.answer('Мы продаем бады')

@dp.message_handler(text = 'Рассчитать')
async def price(message):
    await message.answer('Выберите опцию', reply_markup = start_kb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    images = ['C:\File for Python\1.jpg', 'C:\File for Python\2.jpg', 'C:\File for Python\3.jpg',
              'C:\File for Python\4.jpg',]
    prod_list = crud_fuctions.get_all_product
    for i in prod_list:
        await message.answer(f'Название {title[0]}' | f'Описание {discription[0]}' | f'Цена: {price[0]}')
    with open (images, 'rb') as img:
        await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=catalog_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Поздравляем! Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5; '
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    podschet_kallorii = (10*data['third'])+(6.25*data['second'])-(5*data['first'])+5
    await message.answer(f'Ваша суточная норма каллорий составляет: {podschet_kallorii}')
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
