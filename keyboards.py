from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_ru_start_lang_selection = InlineKeyboardButton('🇷🇺 Русский 🇷🇺', callback_data='ru_start')
button_eng_start_lang_selection = InlineKeyboardButton('🇺🇸 English 🇺🇸', callback_data='en_start')

start_lang_selection = InlineKeyboardMarkup().add(button_ru_start_lang_selection, button_eng_start_lang_selection)

button_ru_lang_selection = InlineKeyboardButton('🇷🇺 Русский 🇷🇺', callback_data='ru')
button_eng_lang_selection = InlineKeyboardButton('🇺🇸 English 🇺🇸', callback_data='en')

lang_selection = InlineKeyboardMarkup().add(button_ru_lang_selection, button_eng_lang_selection)

button_usd_rub = InlineKeyboardButton('USD ➡ RUB', callback_data='USDRUB')
button_rub_usd = InlineKeyboardButton('RUB ➡ USD', callback_data='RUBUSD')

button_eur_rub = InlineKeyboardButton('EUR ➡ RUB', callback_data='EURRUB')
button_rub_eur = InlineKeyboardButton('RUB ➡ EUR', callback_data='RUBEUR')

button_usd_eur = InlineKeyboardButton('USD ➡ EUR', callback_data='USDEUR')
button_eur_usd = InlineKeyboardButton('EUR ➡ USD', callback_data='EURUSD')

cur_keyboard = InlineKeyboardMarkup()
cur_keyboard.add(button_usd_rub, button_usd_eur, button_eur_rub,
                 button_rub_usd, button_eur_usd, button_rub_eur)
