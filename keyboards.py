from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_ru_start_lang_selection = InlineKeyboardButton('🇷🇺 Русский 🇷🇺', callback_data='ru_start')
button_eng_start_lang_selection = InlineKeyboardButton('🇺🇸 English 🇺🇸', callback_data='en_start')

start_lang_selection = InlineKeyboardMarkup().add(button_ru_start_lang_selection, button_eng_start_lang_selection)

button_ru_lang_selection = InlineKeyboardButton('🇷🇺 Русский 🇷🇺', callback_data='ru')
button_eng_lang_selection = InlineKeyboardButton('🇺🇸 English 🇺🇸', callback_data='en')

lang_selection = InlineKeyboardMarkup().add(button_ru_lang_selection, button_eng_lang_selection)
