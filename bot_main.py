import logging
import config
from users_database import add_user, search_user, get_user_lang
from image_parser import parse_image
from place_parser import get_places_coord
from weather_parser import parse_weather
from aiogram import Bot, Dispatcher, executor, types
from keyboards import start_lang_selection, lang_selection
from phrases_get_file import get_phrases


# bot init
bot = Bot(token=config.token)
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
             call.from_user.last_name, call.from_user.username, 'ru')
    await call.message.answer(get_phrases()['ru']['lang_selected'])
    await call.message.answer(get_phrases()['ru']['hello'])
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

@dp.callback_query_handler(text="en_start")
async def start_sel_lang_en(call: types.CallbackQuery):
    add_user(call.from_user.id, call.from_user.first_name,
             call.from_user.last_name, call.from_user.username, 'en')
    await call.message.answer(get_phrases()['en']['lang_selected'])
    await call.message.answer(get_phrases()['en']['hello'])
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

# /select_language
@dp.message_handler(commands=['select_language'])
async def select_lang(message: types.Message):
    return await message.answer(get_phrases()['other']['choose'], reply_markup=lang_selection)

@dp.callback_query_handler(text="ru")
async def sel_lang_ru(call: types.CallbackQuery):
    add_user(call.from_user.id, call.from_user.first_name,
             call.from_user.last_name, call.from_user.username, 'ru')
    await call.message.answer(get_phrases()['ru']['lang_selected'])
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

@dp.callback_query_handler(text="en")
async def sel_lang_ru(call: types.CallbackQuery):
    add_user(call.from_user.id, call.from_user.first_name,
             call.from_user.last_name, call.from_user.username, 'en')
    await call.message.answer(get_phrases()['en']['lang_selected'])
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

# /help command
@dp.message_handler(commands=['h', 'help'])
async def get_help(message: types.Message):
    commands_block = get_phrases()[f'{get_user_lang(message.from_user.id)}']['help']
    return await message.answer('\n'.join(commands_block))


# /image command
@dp.message_handler(commands='image')
async def get_image(message: types.Message):
    image_name = ' '.join(message.text.split(' ')[1::])
    if len(image_name) == 0:
        return await message.answer(get_phrases()[f'{get_user_lang(message.from_user.id)}']['im_error'])
    caption = f'{get_phrases()[f"{get_user_lang(message.from_user.id)}"]["im_desc"]}' + image_name
    return await message.answer_photo(photo=parse_image(image_name), caption=caption)


# /weather command
@dp.message_handler(commands='weather')
async def get_weather(message: types.Message):
    place_name = ' '.join(message.text.split(' ')[1::])
    user_lang_key = f'{get_user_lang(message.from_user.id)}'
    user_key = get_phrases()[user_lang_key]
    if len(place_name) == 0:
        return await message.answer(get_phrases()[f'{user_lang_key}']['wr_error'])
    place_coord = get_places_coord(place_name)
    weather = parse_weather(place_coord)
    weather_list = ['🔍 ' + user_key['wr_search'] + place_name,
                    '🌎 ' + user_key['wr_timezone'] + weather["timezone"],
                    '🌡 ' + user_key['wr_temp'] + weather["temp"],
                    '🌡 ' + user_key['wr_feels'] + weather["temp_feels"],
                    '📈 ' + user_key['wr_press'] + weather["pressure"],
                    '⛅️ ' + user_key['wr_sky'] + weather[f"sky_{user_lang_key}"]]
    weather_message = '\n\n'.join(weather_list)
    return await message.answer(weather_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
