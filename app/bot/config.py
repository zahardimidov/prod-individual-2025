from os import getenv

from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

WEBHOOK_URL = getenv('WEBHOOK_URL')
BOT_TOKEN = getenv('BOT_TOKEN')

emoji = {
    "id": "\U0001F194",
    "calendar": '\U0001F4C5 ',
    "stats": "\U0001F4CA ",
    "search": "\U0001F50D ",
    "nums": "\U0001F522 ",
    "clock": "\U0001F553 ",
    "globe": "\U0001F30D ",
    "restart": "\U0001F504 ",
    "gender": "\U0001F465 ",
    "profile": "\U0001F464 ",
    "like": "\U0001F44D ",
    "pencil": "\u270F ",
    "success": "\u2705 ",
    "internet": "\U0001F310 ",
    "email": "\U0001F4E8 ",
    "wave": "\U0001F44B ",
    'info': "\u2139 ",
    "lock": "\U0001F512 ",
    "unlock": "\U0001F513 ",
    "text": "\U0001F524 ",
    "back": "\U0001F519 ",
    "robot": "\U0001F916 ",
    "warning": "\u26A0 ",
    "sand": "\u23F3 ",
    "star": "\U0001F4AB",
    'upload': '\U0001F4E5 '
}

messages = {
    "profile_btn": emoji['profile'] + 'Профиль',
    "campaigns_btn": emoji['email'] + 'Рекламные кампании',
    "ai_btn": emoji['robot'] + 'Реклама AI',

    "start": emoji["wave"] + "<b>Приветствуем вас в нашем Телеграм-боте!</b>\n"
    f"{emoji["email"]} Здесь рекламодатели могут смотреть, создавать и обновлять рекламные кампании\n"
    f"{emoji["stats"]} А также смотреть статистику.\n",
    "profile": "<b>Ваш профиль</b>\n"+emoji["id"]+"Идентификатор: <code>{advertiser_id}</code>\n"+emoji['text']+"Название: <code>{name}</code>",
    "login": emoji["lock"] + 'Войти в систему',
    "logout": emoji["unlock"] + 'Выйти',
    "campaign_base_info": "<b>Название:</b> {ad_title}\n<b>Текст:</b> {ad_text}\n",
    "details": "Лимит показов: {impressions_limit}\nЛимит переходов: {clicks_limit}\nСтоимость одного показа: {cost_per_impression}\nСтоимость одного перехода: {cost_per_click}\n\n"
    "День начала показа рекламного объявления : {start_date}\nДень окончания показа рекламного объявления: {end_date}\n\n"
    "<b>Настройки таргетирование:</b>\nПол: {gender}\nМинимальный возраст аудитории: {age_from}\nМаксимальный возраст аудитории: {age_to}\nЛокация аудитории: {location}",
    "campaign_stats":
        "Количество уникальных показов: {impressions_count}\nКоличество уникальных переходов: {clicks_count}\nКонверсия в процентах: {conversion}\n"
        "Сумма денег, потраченная на показы: {spent_impressions}\nСумма денег, потраченная на переходы: {spent_clicks}\nОбщая сумма денег, потраченная на кампанию: {spent_total}",
    "try_again": emoji['restart'] + 'Попробовать снова',
    "ai_info": "Я помогу сгенерировать тебе привлекательный текст для твоей рекламы. Тебе нужно всего лишь придумать название",
    "back": emoji['back'] + 'Назад',
    "cancel": "Отменить"
}

class keyboards:
    main = ReplyKeyboardBuilder().add(
        KeyboardButton(text=messages['profile_btn'])).add(
        KeyboardButton(text=messages['campaigns_btn'])).add(
        KeyboardButton(text=messages["ai_btn"])).adjust(2).as_markup(resize_keyboard = True)

    login = InlineKeyboardBuilder().add(InlineKeyboardButton(
        text=messages['login'], callback_data='login')).as_markup()
    logout = InlineKeyboardBuilder().add(InlineKeyboardButton(
        text=messages['logout'], callback_data='logout')).as_markup()
