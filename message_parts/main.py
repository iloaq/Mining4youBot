from bot_utils import get_language_code,get_language_in_db

messages_lang_parts = [
    {
        "lang": "ru",
        "start_message": "Выберите язык",
        "menu": "Приветствую,",
        "calculate": "Расчёт доходности",
        "miners": "Майнеры",
        "miner_place": "Размещение майнеров",
        "order_miner": "Заказать майнер",
        "back": "Назад в меню",
        "contact": "Поделиться контактом",
        "contact_accept": "Спасибо что поделились контактом, с вами свяжутся!",
        "goto_contact": "Перейти к чату",
        "cur_set": "Выберите валюту",
        "select_category": "Валюта:{cur}\nЦена за Kw:{electr}",
        "catalog": "Каталог",
        "settings": "Настройки",
        "cur_set_new": "Введите стоимость kW энергии, или нажите на 'Использовать стандартное значение'",
        "standart_var": "Использовать стандартное значение",
        "back_to_cur": "Назад",
        "stay_electr": "Оставить текущим",
        "cur_set_renew": "На данный момент стоимость электроэнергии {electr}. Если хотите изменить введите стоимость kW энергии, или нажите на 'Использовать стандартное значение'",
        "text_in_miner_miner_place": "Предлагаем разместить ваше оборудование в нашем дата-центре в г.Красноярск.\nСтоимость от 4,32 р за кВт с НДС.\n Доступно к размещению: 10 МВт\nОставляйте заявку по кнопке 'CONTACT'👇",
        "calculate_datas": "🔥Доход в месяц: {dohod} {currency} 💰\n"
                           " ❗Расход за месяц: {rashod} {currency}💵\n"
                           "🔥Прибыль в месяц: {pribyl} {currency}\n"
                           "⚡Окупаемость, месяцев: {okup}\n"
                           "\n"
                           "Расчет на дату и время:\n"
                           "📆 {date} {time}\n"
                           "\n"
                           "\n"
                           "Модель майнера - {name} {th} TH\n"
                           "Цена майнера - {sell} {currency}\n"
                           "При указанной цене за кВТ/ч - {pay} {currency}📌\n"
                           "\n"
                           "Расчёт по курсу Binance 1 BTC = {binancecur} USD\n"
                           "💲Курс  1$ = {courseusd} {currency}\n"
                           "Сложность сети Bitcoin: {dif}\n"
                           "Награда за блок: {reward} BTC\n"
                           "\n"
                           "\n"
                           "Заказать майнеры @diana_miningbtc\n"
                           "🌐http://mining4-you.com\n",
        "other_miner": "Выбрать другой",
        "order_miner": "Заказать майнер",
        "feedback_order": "Для заказа отправьте свой контакт"
    },
    {
        "lang": "en",
        "start_message": "Select language",
        "menu": "Hello,",
        "calculate": "Calculation of profitability",
        "miners": "Miners",
        "miner_place": "Miner placement",
        "order_miner": "Order a miner",
        "contact": "Share contact",
        "contact_accept": "Thanks for sharing your contact, you will be contacted!",
        "back": "back to menu",
        "goto_contact": "Go to chat",
        "cur_set": "Select currency",
        "select_category": "Currency:{cur}\n kW energy cost:{electr}",
        "catalog": "catalog",
        "settings": "Settings",
        "cur_set_new": "Enter the kW energy cost, or click on 'Use standard value'",
        "standart_var": "Use standard value",
        "stay_electr": "Keep current",
        "back_to_cur": "Back",
        "cur_set_renew": "The current value of electricity is {electr}. If you want to change it, enter the kW energy cost, or click on 'Use standard value'",
        "text_in_miner_miner_place": "We offer to place your equipment in our data center in Krasnoyarsk.\nThe cost from 4,32 p per kW with VAT.\n Available for placement: 10 MW\nSubmit an application on the button 'CONTACT'👇",
        "calculate_datas": "🔥Income per month: {dohod} {currency} 💰\n"
                           "❗Monthly expense: {rashod} {currency}💵\n"
                           "🔥Profit per month: {pribyl} {currency}\n"
                           "⚡Payback, months: {okup}\n"
                           "\n"
                           "Calculating for the date and time:\n"
                           "📆 {date} {time}\n"
                           "\n"
                           "\n"
                           "Miner model - {name} {th} TH\n"
                           "Miner price - {sell} {currency}\n"
                           "At the specified price per kWh -\n"
                           " {pay} {currency}📌\n"
                           "\n"
                           "Calculated using Binance exchange rate 1 BTC = {binancecur} USD\n"
                           "💲Course 1$  = {courseusd} {currency}\n"
                           "Bitcoin network complexity: {dif}\n"
                           "Block reward: {reward} BTC\n"
                           "\n"
                           "\n"
                           "Order miners @diana_miningbtc\n"
                           "🌐http://mining4-you.com\n",
        "other_miner": "Select other",
        "order_miner": "Order a miner",
        "feedback_order": "To order, send your contact"
    },
]


def get_message(param, key, auth=False):
    match auth:
        case True:
            lang = get_language_code(get_language_in_db(param))  # Преобразование флагов в коды языков
            for messages in messages_lang_parts:
                if messages["lang"] == lang:
                    return messages[key]
            return None
        case False:
            param = get_language_code(param)  # Преобразование флагов в коды языков
            for messages in messages_lang_parts:
                if messages["lang"] == param:
                    return messages[key]
            return None

