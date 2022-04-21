import logging
import config

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode

from users_database import add_user, search_user, get_user_lang, get_user_city
from image_parser import parse_image
from place_parser import get_places_coord
from currency_parser import get_currency_currate
from weather_parser import parse_weather
from keyboards import start_lang_selection, lang_selection, cur_keyboard
from phrases_get_file import get_phrases


# bot init / 385 sloc
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# /start command
@dp.message_handler(commands="start")
async def start_select_lang(message: types.Message):
    if search_user(message.from_user.id):
        return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['already'])
    return await message.answer(get_phrases()['other']['choose'], reply_markup=start_lang_selection)

@dp.callback_query_handler(text="ru_start")
async def start_sel_lang_ru(call: types.CallbackQuery):
    add_user(call.from_user.id, call.from_user.first_name,
             call.from_user.last_name, call.from_user.username, 'ru', 'not_set')
    await call.message.answer(get_phrases()['ru']['lang_selected'])
    await call.message.answer(get_phrases()['ru']['hello'])
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

@dp.callback_query_handler(text="en_start")
async def start_sel_lang_en(call: types.CallbackQuery):
    add_user(call.from_user.id, call.from_user.first_name,
             call.from_user.last_name, call.from_user.username, 'en', 'not_set')
    await call.message.answer(get_phrases()['en']['lang_selected'])
    await call.message.answer(get_phrases()['en']['hello'])
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

# /select_language command
@dp.message_handler(commands=['select_language'])
async def select_lang(message: types.Message):
    if search_user(message.from_user.id):
        return await message.answer(get_phrases()['other']['choose'], reply_markup=lang_selection)
    else:
        return await message.answer(get_phrases()['other']['not_reg'])

@dp.callback_query_handler(text="ru")
async def sel_lang_ru(call: types.CallbackQuery):
    add_user(call.from_user.id, call.from_user.first_name,
             call.from_user.last_name, call.from_user.username, 'ru', get_user_city(call.from_user.id))
    await call.message.answer(get_phrases()['ru']['lang_selected'])
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

@dp.callback_query_handler(text="en")
async def sel_lang_ru(call: types.CallbackQuery):
    add_user(call.from_user.id, call.from_user.first_name,
             call.from_user.last_name, call.from_user.username, 'en', get_user_city(call.from_user.id))
    await call.message.answer(get_phrases()['en']['lang_selected'])
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

# /help command
@dp.message_handler(commands=['h', 'help'])
async def get_help(message: types.Message):
    if search_user(message.from_user.id):
        commands_block = get_phrases()[f'{get_user_lang(message.from_user.id)}']['help']
        return await message.answer('\n'.join(commands_block))
    else:
        return await message.answer(get_phrases()['other']['help_not_reg'])


# /image command
@dp.message_handler(commands='image')
async def get_image(message: types.Message):
    if search_user(message.from_user.id):
        image_name = ' '.join(message.text.split(' ')[1::])
        if len(image_name) == 0:
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['im_error'])
        caption = f'{get_phrases()[f"{get_user_lang(message.from_user.id)}"]["im_desc"]}' + image_name
        return await message.answer_photo(photo=parse_image(image_name), caption=caption)
    else:
        return await message.answer(get_phrases()['other']['not_reg'])


# /weather command
@dp.message_handler(commands='weather')
async def get_weather(message: types.Message):
    if search_user(message.from_user.id):
        place_name = ' '.join(message.text.split(' ')[1::])
        if len(place_name) == 0 and get_user_city(message.from_user.id) != 'not_set':
            place_name = get_user_city(message.from_user.id)
        user_lang_key = f'{get_user_lang(message.from_user.id)}'
        user_key = get_phrases()[user_lang_key]
        if len(place_name) == 0:
            return await message.answer(get_phrases()[f'{user_lang_key}']['wr_error'])
        place_coord = get_places_coord(place_name)
        weather = parse_weather(place_coord)
        if weather == '/weather argument (place) not found':
            return await message.answer(get_phrases()[f'{user_lang_key}']['wr_ferror'])
        weather_list = ['🔍 ' + text(bold(user_key['wr_search'])) + place_name,
                        '🌎 ' + text(bold(user_key['wr_timezone'])) + weather["timezone"],
                        '🌡 ' + text(bold(user_key['wr_temp'])) + weather["temp"],
                        '🌡 ' + text(bold(user_key['wr_feels'])) + weather["temp_feels"],
                        '📈 ' + text(bold(user_key['wr_press'])) + weather["pressure"],
                        '⛅️ ' + text(bold(user_key['wr_sky'])) + weather[f"sky_{user_lang_key}"]]
        weather_message = '\n\n'.join(weather_list)
        return await message.answer(weather_message, parse_mode=ParseMode.MARKDOWN)
    else:
        return await message.answer(get_phrases()['other']['not_reg'])

# /set_city command
@dp.message_handler(commands='set_city')
async def set_city(message: types.Message):
    if search_user(message.from_user.id):
        us_id = message.from_user.id
        if message.get_args() == 'reset':
            add_user(message.from_user.id, message.from_user.first_name,
                     message.from_user.last_name, message.from_user.username, get_user_lang(message.from_user.id),
                     'not_set')
            return await message.answer(get_phrases()[f"{get_user_lang(us_id)}"]['reset_city'])
        elif message.get_args() != '':
            add_user(message.from_user.id, message.from_user.first_name,
                     message.from_user.last_name, message.from_user.username, get_user_lang(message.from_user.id),
                     ' '.join(message.text.split(' ')[1::]))
            return await message.answer(get_phrases()[f"{get_user_lang(us_id)}"]['set_city'] + message.get_args())
        else:
            return await message.answer(get_phrases()[f"{get_user_lang(us_id)}"]['empty_city'])
    else:
        return await message.answer(get_phrases()['other']['not_reg'])

# /currency command
@dp.message_handler(commands='currency')
async def get_currency(message: types.Message):
    if search_user(message.from_user.id):
        await message.answer(get_phrases()[f"{get_user_lang(message.from_user.id)}"]['set_cur'],
                             reply_markup=cur_keyboard)
    else:
        return await message.answer(get_phrases()['other']['not_reg'])

@dp.callback_query_handler(text="USDRUB")
async def cur_usd_rub(call: types.CallbackQuery):
    await call.message.answer(get_currency_currate("USDRUB"))
    await call.answer()

@dp.callback_query_handler(text="USDEUR")
async def cur_usd_rub(call: types.CallbackQuery):
    await call.message.answer(get_currency_currate("USDEUR"))
    await call.answer()

@dp.callback_query_handler(text="EURRUB")
async def cur_usd_rub(call: types.CallbackQuery):
    await call.message.answer(get_currency_currate("EURRUB"))
    await call.answer()

@dp.callback_query_handler(text="RUBEUR")
async def cur_usd_rub(call: types.CallbackQuery):
    await call.message.answer(get_currency_currate("RUBEUR"))
    await call.answer()

@dp.callback_query_handler(text="EURUSD")
async def cur_usd_rub(call: types.CallbackQuery):
    await call.message.answer(get_currency_currate("EURUSD"))
    await call.answer()

@dp.callback_query_handler(text="RUBUSD")
async def cur_usd_rub(call: types.CallbackQuery):
    await call.message.answer(get_currency_currate("RUBUSD"))
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
