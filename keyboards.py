from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_ru_start_lang_selection = InlineKeyboardButton('๐ท๐บ ะ ัััะบะธะน ๐ท๐บ', callback_data='ru_start')
button_eng_start_lang_selection = InlineKeyboardButton('๐บ๐ธ English ๐บ๐ธ', callback_data='en_start')

start_lang_selection = InlineKeyboardMarkup().add(button_ru_start_lang_selection, button_eng_start_lang_selection)

button_ru_lang_selection = InlineKeyboardButton('๐ท๐บ ะ ัััะบะธะน ๐ท๐บ', callback_data='ru')
button_eng_lang_selection = InlineKeyboardButton('๐บ๐ธ English ๐บ๐ธ', callback_data='en')

lang_selection = InlineKeyboardMarkup().add(button_ru_lang_selection, button_eng_lang_selection)

button_usd_rub = InlineKeyboardButton('USD โก RUB', callback_data='USDRUB')
button_rub_usd = InlineKeyboardButton('RUB โก USD', callback_data='RUBUSD')

button_eur_rub = InlineKeyboardButton('EUR โก RUB', callback_data='EURRUB')
button_rub_eur = InlineKeyboardButton('RUB โก EUR', callback_data='RUBEUR')

button_usd_eur = InlineKeyboardButton('USD โก EUR', callback_data='USDEUR')
button_eur_usd = InlineKeyboardButton('EUR โก USD', callback_data='EURUSD')

cur_keyboard = InlineKeyboardMarkup()
cur_keyboard.add(button_usd_rub, button_usd_eur, button_eur_rub,
                 button_rub_usd, button_eur_usd, button_rub_eur)
