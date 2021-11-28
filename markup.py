from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import  types




#                                              """Main menu"""
main_btn1 = types.KeyboardButton(text=f'Год')
main_btn2 = types.KeyboardButton(text='Месяц')
main_btn3 = types.KeyboardButton(text='Рейтинг')
main_btn4 = types.KeyboardButton(text='Жанр')
main_btn5 = types.KeyboardButton(text='Начать поиск')
kb_main = ReplyKeyboardMarkup(resize_keyboard = True, row_width=2).add(main_btn1,main_btn2,main_btn3,main_btn4,main_btn5)

#                                              """Month Choice"""
btns_months = [None]*12
btns_months[0] = types.InlineKeyboardButton(text='Январь', callback_data='m_JANUARY_Январь')
btns_months[1] = types.InlineKeyboardButton(text='Февраль', callback_data='m_FEBRUARY_Февраль')
btns_months[2] = types.InlineKeyboardButton(text='Март', callback_data='m_MARCH_Март')
btns_months[3] = types.InlineKeyboardButton(text='Апрель', callback_data='m_APRIL_Апрель')
btns_months[4] = types.InlineKeyboardButton(text='Май', callback_data='m_MAY_Май')
btns_months[5] = types.InlineKeyboardButton(text='Июнь', callback_data='m_JUNE_Июнь')
btns_months[6] = types.InlineKeyboardButton(text='Июль', callback_data='m_JULY_Июль')
btns_months[7] = types.InlineKeyboardButton(text='Август', callback_data='m_AUGUST_Август')
btns_months[8] = types.InlineKeyboardButton(text='Сентябрь', callback_data='m_SEPTEMBER_Сентябрь')
btns_months[9] = types.InlineKeyboardButton(text='Октябрь', callback_data='m_OCTOBER_Октябрь')
btns_months[10] = types.InlineKeyboardButton(text='Ноябрь', callback_data='m_NOVEMBER_Ноябрь')
btns_months[11] = types.InlineKeyboardButton(text='Декабрь', callback_data='m_DECEMBER_Декабрь')
kb_month = InlineKeyboardMarkup(one_time_keyboard=True, row_width=3).add(*btns_months)

#                                              """Year Choice"""
btns_years = [None]*9
btns_years[0] = types.InlineKeyboardButton(text='2014', callback_data='y_2014')
btns_years[1] = types.InlineKeyboardButton(text='2015', callback_data='y_2015')
btns_years[2] = types.InlineKeyboardButton(text='2016', callback_data='y_2016')
btns_years[3] = types.InlineKeyboardButton(text='2017', callback_data='y_2017')
btns_years[4] = types.InlineKeyboardButton(text='2018', callback_data='y_2018')
btns_years[5] = types.InlineKeyboardButton(text='2019', callback_data='y_2019')
btns_years[6] = types.InlineKeyboardButton(text='2020', callback_data='y_2020')
btns_years[7] = types.InlineKeyboardButton(text='2021', callback_data='y_2021')
btns_years[8] = types.InlineKeyboardButton(text='2022', callback_data='y_2022')
kb_year = InlineKeyboardMarkup(row_width=3).add(*btns_years)


#                                              """Genre Choice"""
zero = ''
btns_genres = [None]*9
btns_genres[0] = types.InlineKeyboardButton(text='👽 Фантастика', callback_data='g_фантастика')
btns_genres[1] = types.InlineKeyboardButton(text='🤣 Комедия', callback_data='g_комедия')
btns_genres[2] = types.InlineKeyboardButton(text='👻 Ужасы', callback_data='g_ужасы')
btns_genres[3] = types.InlineKeyboardButton(text='🔫 Боевик', callback_data='g_боевик')
btns_genres[4] = types.InlineKeyboardButton(text='🌈 Мультфильм', callback_data='g_мультфильм')
btns_genres[5] = types.InlineKeyboardButton(text='🥲 Драма', callback_data='g_драма')
btns_genres[6] = types.InlineKeyboardButton(text='🔎 Детектив', callback_data='g_детектив')
btns_genres[7] = types.InlineKeyboardButton(text='🚲 Приключения', callback_data='g_приключения')
btns_genres[8] = types.InlineKeyboardButton(text='Любой', callback_data=f'g_{zero}_любой')
kb_genre = InlineKeyboardMarkup(row_width=2).add(*btns_genres)

#                                              """Rating Choice"""
btns_rating = [None]*7
btns_rating[0] = types.InlineKeyboardButton(text='8.0', callback_data='r_8.0')
btns_rating[1] = types.InlineKeyboardButton(text='7.5', callback_data='r_7.5')
btns_rating[2] = types.InlineKeyboardButton(text='7.0', callback_data='r_7.0')
btns_rating[3] = types.InlineKeyboardButton(text='6.5', callback_data='r_6.5')
btns_rating[4] = types.InlineKeyboardButton(text='6.0', callback_data='r_6.0')
btns_rating[5] = types.InlineKeyboardButton(text='5.5', callback_data='r_5.5')
btns_rating[6] = types.InlineKeyboardButton(text='0', callback_data='r_0.0')
kb_rating = InlineKeyboardMarkup(row_width=3).add(*btns_rating)

#                                              """reload"""

btn_start = types.KeyboardButton(text='/reload')
kb_start = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(btn_start)











































