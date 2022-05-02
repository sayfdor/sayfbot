import logging
import config

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode, InputFile

from users_database import add_user, search_user, get_user_lang, get_user_city, get_user_violation
from image_parser import parse_image
from place_parser import get_places_coord
from currency_parser import get_currency_currate, get_currency_pcode, get_lineplot, get_currency_range
from weather_parser import parse_weather
from keyboards import start_lang_selection, lang_selection, cur_keyboard
from phrases_get_file import get_phrases
from obscene_word_check import check


# bot init / 414 strings / 485 - strings + json file
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# /start command
@dp.message_handler(commands="start")
async def start_select_lang(message: types.Message):
    if search_user(message.from_user.id):
        if not config.OFF_ON_COMMANDS['start']:
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['comm_off'])
        return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['already'])
    return await message.answer(get_phrases()['other']['choose'], reply_markup=start_lang_selection)

@dp.callback_query_handler(text="ru_start")
async def start_sel_lang_ru(call: types.CallbackQuery):
    add_user(call.from_user.id, call.from_user.first_name,
             call.from_user.last_name, call.from_user.username, 'ru', 'not_set', 0)
    await call.message.answer(get_phrases()['ru']['lang_selected'])
    await call.message.answer(get_phrases()['ru']['hello'])
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

@dp.callback_query_handler(text="en_start")
async def start_sel_lang_en(call: types.CallbackQuery):
    add_user(call.from_user.id, call.from_user.first_name,
             call.from_user.last_name, call.from_user.username, 'en', 'not_set', 0)
    await call.message.answer(get_phrases()['en']['lang_selected'])
    await call.message.answer(get_phrases()['en']['hello'])
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

# /select_language command
@dp.message_handler(commands=['select_language'])
async def select_lang(message: types.Message):
    if search_user(message.from_user.id):
        if not config.OFF_ON_COMMANDS['sel_lang']:
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['comm_off'])
        return await message.answer(get_phrases()['other']['choose'], reply_markup=lang_selection)
    else:
        return await message.answer(get_phrases()['other']['not_reg'])

@dp.callback_query_handler(text="ru")
async def sel_lang_ru(call: types.CallbackQuery):
    add_user(call.from_user.id, call.from_user.first_name,
             call.from_user.last_name, call.from_user.username,
             'ru', get_user_city(call.from_user.id), get_user_violation(call.from_user.id))
    await call.message.answer(get_phrases()['ru']['lang_selected'])
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

@dp.callback_query_handler(text="en")
async def sel_lang_ru(call: types.CallbackQuery):
    add_user(call.from_user.id, call.from_user.first_name,
             call.from_user.last_name, call.from_user.username,
             'en', get_user_city(call.from_user.id), get_user_violation(call.from_user.id))
    await call.message.answer(get_phrases()['en']['lang_selected'])
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

# /help command
@dp.message_handler(commands=['h', 'help'])
async def get_help(message: types.Message):
    if search_user(message.from_user.id):
        if not config.OFF_ON_COMMANDS['help']:
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['comm_off'])
        if get_user_violation(message.from_user.id, 'bool'):
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['banned'])
        commands_block = get_phrases()[f'{get_user_lang(message.from_user.id)}']['help']
        return await message.answer('\n'.join(commands_block))
    else:
        return await message.answer(get_phrases()['other']['help_not_reg'])


# /image command
@dp.message_handler(commands='image')
async def get_image(message: types.Message):
    if search_user(message.from_user.id):
        if not config.OFF_ON_COMMANDS['image']:
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['comm_off'])
        if get_user_violation(message.from_user.id, 'bool'):
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['banned'])
        image_name = ' '.join(message.text.split(' ')[1::])
        if len(image_name) == 0:
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['im_error'])
        elif check(image_name):
            add_user(message.from_user.id, message.from_user.first_name,
                     message.from_user.last_name, message.from_user.username,
                     get_user_lang(message.from_user.id), get_user_city(message.from_user.id),
                     get_user_violation(message.from_user.id) + 1)
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['bad_word'])
        caption = f'{get_phrases()[f"{get_user_lang(message.from_user.id)}"]["im_desc"]}' + image_name
        return await message.answer_photo(photo=parse_image(image_name), caption=caption)
    else:
        return await message.answer(get_phrases()['other']['not_reg'])


# /weather command
@dp.message_handler(commands='weather')
async def get_weather(message: types.Message):
    if search_user(message.from_user.id):
        if not config.OFF_ON_COMMANDS['weather']:
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['comm_off'])
        if get_user_violation(message.from_user.id, 'bool'):
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['banned'])
        place_name = ' '.join(message.text.split(' ')[1::])
        if len(place_name) == 0 and get_user_city(message.from_user.id) != 'not_set':
            place_name = get_user_city(message.from_user.id)
        elif check(place_name):
            add_user(message.from_user.id, message.from_user.first_name,
                     message.from_user.last_name, message.from_user.username,
                     get_user_lang(message.from_user.id), get_user_city(message.from_user.id),
                     get_user_violation(message.from_user.id) + 1)
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['bad_word'])
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
        if not config.OFF_ON_COMMANDS['set_city']:
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['comm_off'])
        if get_user_violation(message.from_user.id, 'bool'):
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['banned'])
        us_id = message.from_user.id
        if message.get_args() == 'reset':
            add_user(message.from_user.id, message.from_user.first_name,
                     message.from_user.last_name, message.from_user.username, get_user_lang(message.from_user.id),
                     'not_set', get_user_violation(message.from_user.id))
            return await message.answer(get_phrases()[f"{get_user_lang(us_id)}"]['reset_city'])
        elif check(message.get_args()):
            add_user(message.from_user.id, message.from_user.first_name,
                     message.from_user.last_name, message.from_user.username,
                     get_user_lang(message.from_user.id), get_user_city(message.from_user.id),
                     get_user_violation(message.from_user.id) + 1)
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['bad_word'])
        elif message.get_args() != '':
            add_user(message.from_user.id, message.from_user.first_name,
                     message.from_user.last_name, message.from_user.username, get_user_lang(message.from_user.id),
                     ' '.join(message.text.split(' ')[1::]), get_user_violation(message.from_user.id))
            return await message.answer(get_phrases()[f"{get_user_lang(us_id)}"]['set_city'] + message.get_args())
        else:
            return await message.answer(get_phrases()[f"{get_user_lang(us_id)}"]['empty_city'])
    else:
        return await message.answer(get_phrases()['other']['not_reg'])

# /simple_currency command
@dp.message_handler(commands='currency')
async def get_simple_currency(message: types.Message):
    if search_user(message.from_user.id):
        if not config.OFF_ON_COMMANDS['currency']:
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['comm_off'])
        if get_user_violation(message.from_user.id, 'bool'):
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['banned'])
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

@dp.message_handler(commands='currency_plot')
async def get_currency(message: types.Message):
    if search_user(message.from_user.id):
        if not config.OFF_ON_COMMANDS['currency_plot']:
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['comm_off'])
        if get_user_violation(message.from_user.id, 'bool'):
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['banned'])
        message_args = message.text.split(' ')[1::]

        if len(message_args) == 0:
            return await message.answer(get_phrases()[get_user_lang(message.from_user.id)]['hcur_null_error'])

        elif check(''.join(message_args)):
            add_user(message.from_user.id, message.from_user.first_name,
                     message.from_user.last_name, message.from_user.username,
                     get_user_lang(message.from_user.id), get_user_city(message.from_user.id),
                     get_user_violation(message.from_user.id) + 1)
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['bad_word'])

        elif message_args[0] in ['all', '-a', 'a']:
            return await message.answer(get_currency_pcode('all', get_user_lang(message.from_user.id)))

        elif len(get_currency_pcode(message_args[0].upper())) != 0\
                and get_currency_pcode(message_args[0].upper()) != 'error':
            plot = get_lineplot(get_currency_range(message_args[0].upper(), message_args[1]), message.from_user.id)
            if plot == ['error']:
                return await message.answer(get_phrases()[get_user_lang(message.from_user.id)]['hcur_range_error'])
            return await message.answer_photo(photo=InputFile(f"plots/{message.from_user.id}_plot.png"))

        else:
            return await message.answer(get_phrases()[get_user_lang(message.from_user.id)]['hcur_error'])

    else:
        return await message.answer(get_phrases()['other']['not_reg'])

@dp.message_handler()
async def simple_message(message: types.Message):
    if search_user(message.from_user.id):
        if not config.OFF_ON_COMMANDS['simple_message']:
            return None
        if get_user_violation(message.from_user.id, 'bool'):
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['banned'])
        if check(message.text):
            add_user(message.from_user.id, message.from_user.first_name,
                     message.from_user.last_name, message.from_user.username,
                     get_user_lang(message.from_user.id), get_user_city(message.from_user.id),
                     get_user_violation(message.from_user.id) + 1)
            return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['bad_word'])
        return await message.answer(get_phrases()[get_user_lang(message.from_user.id)]['dont_speak'])
    else:
        return await message.answer(get_phrases()['other']['not_reg'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
