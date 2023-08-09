from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from message_parts.main import get_message
from bot_utils import get_language_in_db
from CBDate import callbackdata_order_miner, callbackdata_settings, callbackdata_calculate_miner
class keyboard_start():
    ru = KeyboardButton('🇷🇺')
    us = KeyboardButton('🇺🇸')
    start_button = ReplyKeyboardMarkup(resize_keyboard=True).add(ru,us)

class keyboard_menu():
    def return_menu(param, auth=False):
        if auth:
            language = get_language_in_db(param)
        else:
            language = param
        miner_price = KeyboardButton(f'{get_message(language, "miners")}')
        miner_place = KeyboardButton(f'{get_message(language, "miner_place")}')
        order_miner = KeyboardButton(f'{get_message(language, "order_miner")}')
        menu = ReplyKeyboardMarkup(resize_keyboard=True).add(miner_price,miner_place,order_miner)
        return menu

class miner_place_button():
    def return_button(param, auth=False):
        if auth:
            language = get_language_in_db(param)
        else:
            language = param
        back = KeyboardButton(f'{get_message(language, "back")}')
        contact = KeyboardButton(f'{get_message(language, "contact")}',request_contact=True)
        button = ReplyKeyboardMarkup(resize_keyboard=True).add(back,contact)
        return button

class miner_order_button():
    def return_button(param, auth=False):
        if auth:
            language = get_language_in_db(param)
        else:
            language = param
        back = InlineKeyboardButton(f'{get_message(language, "back")}',callback_data=callbackdata_order_miner.new('back'))
        contact = InlineKeyboardButton(f'{get_message(language, "goto_contact")}',url='https://t.me/diana_miningbtc',callback_data=callbackdata_order_miner.new('contact'))
        button = InlineKeyboardMarkup(row_width=1).add(contact,back)
        return button

class calatol_miner():
    def return_button(param, auth=False):
        if auth:
            language = get_language_in_db(param)
        else:
            language = param
        catalog = InlineKeyboardButton(f'{get_message(language, "catalog")}', switch_inline_query_current_chat='')
        setting = InlineKeyboardButton(f'{get_message(language, "settings")}', callback_data = callbackdata_settings.new())
        button = InlineKeyboardMarkup(row_width=1).add(catalog,setting)
        return button

class cur_select_button():
    rub_button = KeyboardButton('RUB')
    usd_button = KeyboardButton(f'USD',)
    button = ReplyKeyboardMarkup(row_width=1).add(rub_button,usd_button)

class electr_select_button():
    def return_button(param, stay=False, auth=False):
        if auth:
            language = get_language_in_db(param)
        else:
            language = param
        standart_button = KeyboardButton(f'{get_message(language, "standart_var")}')
        button = ReplyKeyboardMarkup(resize_keyboard=True).add(standart_button)

        if stay:
            stay_button = KeyboardButton(f'{get_message(language, "stay_electr")}')
            button.add(stay_button)

        return button
    
class inline_result_miners():
    def return_button(param, id, auth=False):
        if auth:
            language = get_language_in_db(param)
        else:
            language = param
        calculate = InlineKeyboardButton(f'{get_message(language, "calculate")}',callback_data=callbackdata_calculate_miner.new('calculate',id))
        share = InlineKeyboardButton(f'{get_message(language, "order_miner")}',callback_data=callbackdata_calculate_miner.new('share',id))
        button = InlineKeyboardMarkup(row_width=1).add(calculate,share)
        return button