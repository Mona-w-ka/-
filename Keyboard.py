from telebot import types

def menu_main():
    buttons = ["Баланс", "Перевод", "Курс", "Отзыв"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(btn) for btn in buttons])
    return markup

def menu_crypto():
    buttons = ["BTC", "TON", "ETH", "Назад⬅️"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(btn) for btn in buttons])
    return markup

def menu_not_wallet():
    buttons = ["Добавить кошелек","Назад⬅️"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(btn) for btn in buttons])
    return markup

def menu_transactions():
    buttons = ["Совершить перевод", "Добавить кошелек", "Назад⬅️"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(btn) for btn in buttons])
    return markup

def menu_send_transaction():
    buttons = ["Между своими", "Другому юзеру", "Назад⬅️"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[types.KeyboardButton(btn) for btn in buttons])
    return markup