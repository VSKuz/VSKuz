#@title Полный код бота для самоконтроля
import aiosqlite
import asyncio
import logging
import quiz_questions
from gen_opt_key import generate_options_keyboard
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

with open("token.txt") as tok:
# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
    API_TOKEN = tok.read()

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

# Хэндлер на команду /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    #Отправка ответного сообщения
    await message.answer(f"Давайте начнем квиз!")
    #Создание нового квиза
    await new_quiz(message)
    
#Функция создания нового квиза
async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    current_result = 0
    await update_quiz_index(user_id, current_question_index)
    await update_result(user_id, current_result)
    await get_question(message, user_id)

# Зададим имя базы данных
DB_NAME = 'quiz_bot.db'
DB_RESULT = 'quiz_player_result.db'

# Структура квиза
quiz_data = quiz_questions.quiz_qdb()

async def create_table():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        # Сохраняем изменения
        await db.commit()

async def create_score():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_RESULT) as db:
        # Создаем таблицу
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, result INTEGER)''')
        # Сохраняем изменения
        await db.commit()


#Функция получения вопроса для текущего пользователя
async def get_question(message, user_id):
    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)




@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    await callback.message.answer("Верно!")
    current_question_index = await get_quiz_index(callback.from_user.id)
    curent_question_result = await get_quiz_result(callback.from_user.id)
    # Обновление номера текущего вопроса и результата в базе данных
    current_question_index += 1
    curent_question_result += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    await update_result(callback.from_user.id, curent_question_result)


    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await callback.message.answer("Ваш результат: ", curent_question_result ,"из ", len(quiz_data))


@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )


    # Получение текущего вопроса и результата из словаря состояний пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    curent_question_result = await get_quiz_result(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса результата в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await callback.message.answer("Ваш результат: ", curent_question_result ," из ", len(quiz_data))



async def get_question(message, user_id):

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)


async def get_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def get_quiz_result(user_id):
    # Подключаемся к базе данных
    async with aiosqlite.connect(DB_RESULT) as db:
        async with db.execute('SELECT result FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor1:
            # Возвращаем результат
            results1 = await cursor1.fetchone()
            if results1 is not None:
                return int(results1[0])
            else:
                return 0

async def update_quiz_index(user_id, index):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Сохраняем изменения
        await db.commit()

async def update_result(user_id, result):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_RESULT) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, result) VALUES (?, ?)', (user_id, result))
        # Сохраняем изменения
        await db.commit()

# Запуск процесса поллинга новых апдейтов
async def main():

    # Запускаем создание таблицы базы данных
    await create_table()
    await create_score()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())