import logging

from aiogram import Bot,types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from states import Language, calculate_datas, order_miner_state
from keyboards.main import keyboard_start, keyboard_menu, miner_place_button, miner_order_button, calatol_miner, cur_select_button, electr_select_button, calculate_buttons_result, feedback_buttons
from message_parts.main import get_message, messages_lang_parts
from db import dbase
from CBDate import callbackdata_order_miner, callbackdata_settings, callbackdata_calculate_miner,callbackdata_calculate_miner_result
from inline_utils import create_inline_results
from WooAPi import get_all_products
from bot_utils import get_miner_data,get_api_data,datetimedef,get_miner_info, create_contact_amo, create_lead_and_link_to_contact, get_language_in_db

API_TOKEN = '5505744557:AAFAF1qlsOAG3XXwhhFOTkIZbs_bUR9bDr0'

# webhook settings
WEBHOOK_HOST = 'https://2786-92-55-161-246.ngrok.io'
WEBHOOK_PATH = '/api'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 8000

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    locale = message.from_user.locale
    await Language.language.set()
    await bot.send_message(message.chat.id, f'{get_message(locale.language, "start_message")}', reply_markup= keyboard_start.start_button)

@dp.message_handler(content_types=['text'], state=Language)
async def menu(message: types.Message, state: FSMContext):
    await state.update_data(language=message.text)
    dbase.insert_user(user_id=message.chat.id, lang=message.text)
    await bot.send_message(message.chat.id,f'{get_message(message.text, "menu")}{message.chat.username}', reply_markup= keyboard_menu.return_menu(message.text))
    await state.finish()

@dp.message_handler(lambda message: message.text in [get_message(lg, "miner_place") for lg in ('ru', 'en')], state='*')
async def miner_place(message: types.Message):
    await bot.send_message(message.chat.id, f'{get_message(message.chat.id, "text_in_miner_miner_place",True)}', reply_markup= miner_place_button.return_button(message.chat.id,True) )    

@dp.message_handler(lambda message: message.text in [get_message(lg, "back") for lg in ('ru', 'en')], state='*')
async def miner_place_use(message: types.Message):
    await message.delete()
    await bot.send_message(message.chat.id,f'{get_message(message.chat.id, "menu",True)}{message.chat.username}', reply_markup= keyboard_menu.return_menu(message.chat.id, True))

@dp.message_handler(content_types='contact', state='*')
async def miner_place_use(message: types.Message, state: FSMContext):
    data = await state.get_data()
    miner = data.get('miner', None)
    price = data.get('price', 0)
    contact = create_contact_amo(message.from_user.username,message.contact.phone_number, miner=miner,lang=get_language_in_db(message.from_user.id), price= dbase.select(message.from_user.id, "electricity")[0],curr=dbase.select(message.from_user.id, "currency")[0],telegram_id=message.from_user.id, telegram_url=message.from_user.username)
    create_lead_and_link_to_contact(contact, miner, name=f'Заказ пользователя {contact}', price=price)
    await bot.send_message(message.chat.id,f'{get_message(message.chat.id, "contact_accept",True)}', reply_markup= keyboard_menu.return_menu(message.chat.id, True))


@dp.message_handler(lambda message: message.text in [get_message(lg, "miners") for lg in ('ru', 'en')], state='*')
async def miner_price(message: types.Message):
    chat_id = message.chat.id
    electr, cur = dbase.select(chat_id, "electricity, currency")
    if cur is None or electr is None:
        await calculate_datas.cur.set()
        await bot.send_message(chat_id, get_message(chat_id, "cur_set", True), reply_markup=cur_select_button.button)
    else:
        select_category_text = get_message(chat_id, "select_category", True)
        await bot.send_message(chat_id, f"{select_category_text.format(cur=cur,electr=electr)}",reply_markup=calatol_miner.return_button(message.chat.id,True))

@dp.message_handler(lambda message: message.text in [get_message(lg, "order_miner") for lg in ('ru', 'en')], state='*')
async def order_miner(message: types.Message):
    await bot.send_message(message.chat.id, f'😇',reply_markup= miner_order_button.return_button(message.chat.id,True)) 


@dp.message_handler(lambda message: message.text in ['USD', 'RUB'], state=calculate_datas.cur)
async def cur_set(message: types.Message, state: FSMContext):
    dbase.insert_user(message.chat.id,currency=message.text)
    electr = dbase.select(message.chat.id,'electricity')
    if electr[0] is None:
        await bot.send_message(message.chat.id, f'{get_message(message.chat.id, "cur_set_new",True)}',reply_markup=electr_select_button.return_button(message.chat.id, auth=True))
        await calculate_datas.next()
    else:
        select_cur_renew_text = get_message(message.chat.id, "cur_set_renew", True)
        await bot.send_message(message.chat.id, f'{select_cur_renew_text.format(electr=electr)}', reply_markup=electr_select_button.return_button(message.chat.id, True, True)) #добавит кнопки
        await calculate_datas.next()

@dp.message_handler(lambda message: message.text.replace('.', '', 1).isdigit(), state=calculate_datas.electr)
async def electr_set(message: types.Message, state: FSMContext):
    dbase.insert_user(message.chat.id,electricity=message.text)
    await state.finish()
    await message.delete_reply_markup()
    electr, cur = dbase.select(message.chat.id, "electricity, currency")
    select_category_text = get_message(message.chat.id, "select_category", True)
    await bot.send_message(message.chat.id, f"{select_category_text.format(cur=cur,electr=electr)}",reply_markup=calatol_miner.return_button(message.chat.id,True))

@dp.message_handler(lambda message: message.text in [get_message(lg, "standart_var") for lg in ('ru', 'en')], state=calculate_datas.electr)
async def electr_set_deaful(message: types.Message, state: FSMContext):
    await state.finish()
    dbase.insert_user(message.chat.id,electricity=4.32)
    electr, cur = dbase.select(message.chat.id, "electricity, currency")
    select_category_text = get_message(message.chat.id, "select_category", True)
    await bot.send_message(message.chat.id, f"{select_category_text.format(cur=cur,electr=electr)}",reply_markup=calatol_miner.return_button(message.chat.id,True))

@dp.message_handler(lambda message: message.text in [get_message(lg, "back_to_cur") for lg in ('ru', 'en')], state=calculate_datas.electr)
async def electr_set_deaful(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, get_message(message.chat.id, "cur_set", True), reply_markup=cur_select_button.button)
    await calculate_datas.cur.set()

@dp.message_handler(lambda message: message.text in [get_message(lg, "stay_electr") for lg in ('ru', 'en')], state=calculate_datas.electr)
async def electr_set_deaful(message: types.Message, state: FSMContext):
    await state.finish()
    electr, cur = dbase.select(message.chat.id, "electricity, currency")
    select_category_text = get_message(message.chat.id, "select_category", True)
    await bot.send_message(message.chat.id, f"{select_category_text.format(cur=cur,electr=electr)}",reply_markup=calatol_miner.return_button(message.chat.id,True))

@dp.callback_query_handler(callbackdata_settings.filter())
async def settings_miners(callback: types.CallbackQuery, callback_data: dict):
        match callback_data['method']:
            case 'catalog':
                pass
            case 'settings':
                await calculate_datas.cur.set()
                await callback.message.delete()
                await bot.send_message(callback.message.chat.id, get_message(callback.message.chat.id, "cur_set", True), reply_markup=cur_select_button.button)

@dp.callback_query_handler(callbackdata_order_miner.filter())
async def order_miner_cb(callback: types.CallbackQuery, callback_data: dict):
    match callback_data['method']:
        case 'contact':
            await callback.message.delete()
            await bot.send_message(callback.message.chat.id,f'{get_message(callback.message.chat.id, "menu",True)}{callback.message.chat.username}', reply_markup= keyboard_menu.return_menu(callback.message.chat.id, True))
        case 'back':
            await callback.message.delete()
            await bot.send_message(callback.message.chat.id,f'{get_message(callback.message.chat.id, "menu",True)}{callback.message.chat.username}', reply_markup= keyboard_menu.return_menu(callback.message.chat.id, True))

@dp.callback_query_handler(callbackdata_calculate_miner.filter())
async def calculate_miner_callback(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    match callback_data['method']:
        case 'calculate':
            product_id = callback_data['id']
            currency, electricity = dbase.select(callback.from_user.id,"currency, electricity")
            binancecrs, courseusd, dif, reward, reward1th = get_api_data(currency).values()
            dohod,rashod,pribyl,okup,name,th = get_miner_data(product_id,callback.from_user.id).values()
            date, time = datetimedef().values()
            minername,sell,cost,ths= get_miner_info(product_id, currency).values()
            select_category_text = get_message(callback.from_user.id, "calculate_datas", True)
            await bot.send_message(callback.from_user.id, f"{select_category_text.format(dohod=dohod,sell = sell,rashod=rashod,pribyl=pribyl,okup=okup,name=name,th=th,binancecur=binancecrs,courseusd = courseusd,dif = dif, reward = reward, reward1th = reward1th, currency = currency, pay = electricity,date=date,time=time)}", reply_markup= calculate_buttons_result.return_button(callback.from_user.id,product_id,True))
        case 'share':
            product_id = callback_data['id']
            minername,sell,cost,ths= get_miner_info(product_id, 'RUB').values()
            await order_miner_state.miner.set()
            await state.update_data(miner=minername+''+ths)
            await order_miner_state.price.set()
            await state.update_data(price=cost)
            await bot.send_message(callback.from_user.id,get_message(callback.from_user.id, "feedback_order", True),reply_markup=feedback_buttons.return_button(callback.from_user.id,True))

@dp.callback_query_handler(callbackdata_calculate_miner_result.filter())
async def feedback(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    match callback_data['method']:
        case 'order':
            product_id = callback_data['title']
            minername,sell,cost,ths= get_miner_info(product_id, 'RUB').values()
            await order_miner_state.miner.set()
            await state.update_data(miner=minername+''+ths)
            await order_miner_state.price.set()
            await state.update_data(price=cost)
            await bot.send_message(callback.from_user.id,get_message(callback.from_user.id, "feedback_order", True),reply_markup=feedback_buttons.return_button(callback.from_user.id,True))
        case 'settings':
            await calculate_datas.cur.set()
            await callback.message.delete()
            await bot.send_message(callback.from_user.id, get_message(callback.from_user.id, "cur_set", True), reply_markup=cur_select_button.button)
        case 'back':
            await callback.message.delete()
            await bot.send_message(callback.from_user.id,f'{get_message(callback.from_user.id, "menu",auth=True)}{callback.from_user.username}', reply_markup= keyboard_menu.return_menu(callback.from_user.id,True))

@dp.inline_handler()
async def inline_query_handler(query: types.InlineQuery):
    
    # Get products from the WooCommerce store with lang='ru'
    products = get_all_products('ru')

    # Create a list of results based on the products
    results = create_inline_results(products,query.from_user.id)

    # Send the response to the inline query
    await bot.answer_inline_query(query.id, results)
    


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info('Starting..')


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Done!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )