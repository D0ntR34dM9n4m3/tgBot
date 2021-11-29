import logging
import aiogram.utils.markdown as fmt
from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot import api
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import telegram_api
import markup
from bot import run, get_movie_url_year_name, get_trailer, get_kp_trailer   # get_trailer и get_kp_trailer взаимозаменяемы
from markup import kb_month

bot = Bot(token=telegram_api)
dp = Dispatcher(bot, storage=MemoryStorage())

class FSMuser(StatesGroup):
    state_main = State()
    state_searching = State()


@dp.message_handler(commands=['help'], state=FSMuser.state_main)
@dp.message_handler(commands=['help'], state=None)
async def command_help(message: types.Message, state: FSMContext):
    await message.reply('Вас приветствует бот для поиска новинок (и не только) в индустрии кино!\n\n'
                        'Чтобы начать поиск, нужно ввести два необходимых параметра - год и месяц цифрового релиза фильма. '
                        'После окончания поиска, Вы также можете более подробно изучить результаты, '
                        'нажатием на кнопку с названием фильма, после чего, можно еще и найти трейлер к нему!\n\n'
                        'Список команд:\n'
                        '/start - для начала работы с ботом,\n'
                        '/reload - сбрасывает все введенные данные\n'
                        '/help - для вызова меню списка команд\n\n'
                        'ВНИМАНИЕ! При отправке сообщения со ссылкой от бота, '
                        'сообщение может приходить пустым или без ссылки, если такое происходит, '
                        'попробуйте просто нажать кнопку повторно.\n\nУдачи! 😉')



@dp.message_handler(commands=['start', 'старт'], state=FSMuser.state_main)
@dp.message_handler(commands=['start', 'старт'], state=None)
async def command_start(message: types.Message, state: FSMContext):
    await FSMuser.state_main.set()
    async with state.proxy() as data:
        data['movies'] = []
        data['chosen_month'] = 'не выбран'
        data['month'] = None
        data['chosen_year'] = 'не выбран'
        data['year'] = None
        data['rating'] = 0
        data['genre'] = ''
        data['chosen_genre'] = 'любой'
    await bot.send_message(message.from_user.id, 'Привет, {0.first_name}!\nПо каким параметрам будем искать фильмы?'.format(message.from_user), reply_markup=markup.kb_main)


@dp.message_handler(commands=['reload', 'обновить'], state=FSMuser.state_main)
@dp.message_handler(commands=['reload', 'обновить'], state=None)
async def command_reload(message: types.Message, state: FSMContext):
    await state.finish()
    await FSMuser.state_main.set()
    async with state.proxy() as data:
        data['movies'] = []
        data['chosen_month'] = 'не выбран'
        data['month'] = None
        data['year'] = None
        data['chosen_year'] = 'не выбран'
        data['rating'] = 0
        data['genre'] = ''
        data['chosen_genre'] = 'любой'
    await message.reply('Все введенные данные обновлены', reply_markup=markup.kb_main)

@dp.message_handler(Text(equals='месяц', ignore_case=True), state=FSMuser.state_main)
async def command_month(message: types.Message, state: FSMContext):
    await message.reply('Выбери из списка ниже', reply_markup=markup.kb_month)

@dp.message_handler(Text(equals='Год и месяц', ignore_case=True), state=FSMuser.state_main)
async def command_year(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.reply(f'Текущее значение: месяц <b>{data["chosen_month"]}</b>, год <b>{data["chosen_year"]}</b>', reply_markup=markup.kb_year, parse_mode='html')

@dp.message_handler(Text(equals='жанр', ignore_case=True), state=FSMuser.state_main)
async def command_genre(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.reply(f'Текущее значение - <b>{data["chosen_genre"]}</b>, его можно изменить', reply_markup=markup.kb_genre, parse_mode='html')

@dp.message_handler(Text(equals='рейтинг', ignore_case=True), state=FSMuser.state_main)
async def command_rating(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.reply(f'Текущее значение - <b>{data["rating"]}</b>, его можно изменить', reply_markup=markup.kb_rating, parse_mode='html')


@dp.message_handler(Text(equals='начать поиск', ignore_case=True), state=FSMuser.state_main)
async def command_parse(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['month'] and data['year']:
            kb_main = types.ReplyKeyboardRemove()
            await message.reply('Подожди немного...', reply_markup=kb_main)
            await FSMuser.state_searching.set()
            data = await run(data)

                                                        # Клавиатура со списком фильмов
            btns_movie = [None] * len(data['movies'])
            count = 0                                   # каунтер для кнопок
            for i in data['movies']:
                btns_movie[count] = types.InlineKeyboardButton(text=f'{round(i.rating, 1)}  {i.nameRu}', callback_data=f'f_{i.id}')
                count += 1
            kb_movie = InlineKeyboardMarkup(row_width=1).add(*btns_movie)
            if count == 0:
                await message.answer('К сожалению, поиск не дал результатов :(')
            else:
                await message.answer('Поиск успешно окончен! Вот результаты, которые можно изучить подробнее:', reply_markup=kb_movie)


            await FSMuser.state_main.set()
            await message.answer('Обращайся еще :)', reply_markup=markup.kb_start)
        elif data['year'] == None and data['month']:
            await message.answer('Нужно выбрать год!')
        elif data['month'] == None and data['year']:
            await message.answer('Нужно выбрать месяц!')
        elif data['month'] == None and data['year'] == None:
            await message.answer('Сначала нужно выбрать год и месяц!')


def movie_info(id, data):
    for movie in data['movies']:
        if movie.id == id:
            genres = str(movie.genres)
            genres = genres.replace('[', '').replace(']', '').replace('\'', '')
            countries = str(movie.countries)
            countries = countries.replace('[', '').replace(']', '').replace('\'', '')
            rating = round(movie.rating, 1)

    link, year, name = get_movie_url_year_name(id)
    link = fmt.hide_link(link)
    msg_text = f"{link}{countries}  {rating}\n({genres})"
    return msg_text


@dp.callback_query_handler(state=None)
@dp.callback_query_handler(state=FSMuser.state_main)
async def cmd_callback(call: types.CallbackQuery, state: FSMContext):
    msg = call.data
    value = msg.split("_")[-1]
    month = msg.split("_")[1]
    any_genre = msg.split("_")[1]
    if msg.startswith('m_'):
        async with state.proxy() as data:
            data['month'] = month
            data['chosen_month'] = value
        await call.message.edit_reply_markup()
        await call.message.answer(f'Месяц: <b>{value}</b>', parse_mode='html')
    if msg.startswith('y_'):
        async with state.proxy() as data:
            data['year'] = value
            data['chosen_year'] = value
        await call.message.edit_reply_markup(reply_markup=kb_month)
        await call.message.answer(f'Год <b>{value}</b>-й', parse_mode='html')
    if msg.startswith('g_'):
        if any_genre == '':
            async with state.proxy() as data:
                data['genre'] = ''
                data['chosen_genre'] = 'любой'
        else:
            async with state.proxy() as data:
                data['genre'] = value
                data['chosen_genre'] = value
        await call.message.edit_reply_markup()
        await call.message.answer(f'Будем искать фильмы в жанре "<b>{value}</b>"!', parse_mode='html')
    if msg.startswith('r_'):
        async with state.proxy() as data:
            data['rating'] = value
        await call.message.edit_reply_markup()
        await call.message.answer(f'С рейтингом <b>{value}</b> и выше', parse_mode='html')
    if msg.startswith('f_'):
        async with state.proxy() as data:
            link, year, name = get_movie_url_year_name(value)
            btn_trailer = types.InlineKeyboardButton(text=f'Найти трейлер', callback_data=f't_{value}')
            kb_trailer = InlineKeyboardMarkup(row_width=2, resize_keyboard=True).add(btn_trailer)
            try:
                await call.message.answer(f"{movie_info(value, data)}", parse_mode=types.ParseMode.HTML, reply_markup=kb_trailer)
            except UnboundLocalError:
                await call.message.answer("Эти кнопки уже устарели...", parse_mode=types.ParseMode.HTML)
            except Exception:
                await call.message.answer(f"{movie_info(value, data)}", parse_mode=types.ParseMode.HTML)


    if msg.startswith('t_'):

        await call.message.answer(f"{(fmt.hide_link(await get_trailer(value)))}", parse_mode=types.ParseMode.HTML)

    await call.answer(text='Информация обновилась')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

