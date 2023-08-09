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
        "goto_contact": "Перейти к чату",
        "cur_set": "Выберите валюту",
        "select_category": "Валюта:{cur}",
        "catalog": "Каталог",
        "settings": "Настройки",
        "cur_set_new": "Введите стоимость kW энергии, или нажите на 'Использовать стандартное значение'",
        "standart_var": "Использовать стандартное значение",
        "stay_electr": "Оставить текущим",
        "cur_set_renew": "На данный момент стоимость электроэнергии {electr}. Если хотите изменить введите стоимость kW энергии, или нажите на 'Использовать стандартное значение'",
        "text_in_miner_miner_place": "Предлагаем разместить ваше оборудование в нашем дата-центре в г.Красноярск.\nСтоимость от 4,32 р за кВт с НДС.\n Доступно к размещению: 10 МВт\nОставляйте заявку по кнопке 'CONTACT'👇",
        "calculate_datas": "🔥Доход в месяц: {dohod} {currency} 💰"
                           " ❗Расход за месяц: {rashod} {currency}💵"
                           "🔥Прибыль в месяц: {pribyl} {currency}"
                           "⚡Окупаемость, месяцев: {okup}"
                           ""
                           "Расчет на дату и время:"
                           "📆 {date} {time}"
                           ""
                           ""
                           "Модель майнера - {name} {th} TH"
                           "Цена майнера - {sell} {currency}"
                           "При указанной цене за кВТ/ч - {pay} {currency}📌"
                           ""
                           "Расчёт по курсу Binance 1 BTC = {binancecur} USD"
                           "💲Курс  1$ = {courseusd} {currency}"
                           "Сложность сети Bitcoin: {dif}"
                           "Награда за блок: {reward} BTC"
                           ""
                           ""
                           "Заказать майнеры @diana_miningbtc "
                           "🌐http://mining4-you.com",
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
        "back": "back to menu",
        "goto_contact": "Go to chat",
        "cur_set": "Select currency",
        "select_category": "Валюта:{cur}",
        "catalog": "catalog",
        "settings": "Settings",
        "cur_set_new": "Enter the kW energy cost, or click on 'Use standard value'",
        "standart_var": "Use standard value",
        "stay_electr": "Keep current",
        "cur_set_renew": "The current value of electricity is {electr}. If you want to change it, enter the kW energy cost, or click on 'Use standard value'",
        "text_in_miner_miner_place": "We offer to place your equipment in our data center in Krasnoyarsk.\nThe cost from 4,32 p per kW with VAT.\n Available for placement: 10 MW\nSubmit an application on the button 'CONTACT'👇",
        "calculate_datas": "🔥Income per month: {dohod} {currency} 💰"
                           "❗Monthly expense: {rashod} {currency}💵"
                           "🔥Profit per month: {pribyl} {currency}"
                           "⚡Payback, months: {okup}"
                           ""
                           "Calculating for the date and time:"
                           "📆 {date} {time}"
                           ""
                           ""
                           "Miner model - {name} {th} TH"
                           "Miner price - {sell} {currency}"
                           "At the specified price per kWh -"
                           " {pay} {currency}📌"
                           ""
                           "Calculated using Binance exchange rate 1 BTC = {binancecur} USD"
                           "💲Course 1$  = {courseusd} {currency}"
                           "Bitcoin network complexity: {dif}"
                           "Block reward: {reward} BTC"
                           ""
                           ""
                           "Order miners @diana_miningbtc"
                           "🌐http://mining4-you.com",
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

