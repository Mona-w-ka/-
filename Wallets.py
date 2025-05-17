from telebot import types
import models
import Keyboard
import Bchain


def ask_for_wallet_address(bot, chat_id, next_step="add"):
    bot.send_message(
        chat_id,
        "Введите адрес вашего кошелька:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    return {"next_step": next_step}


def find_full_wallet_address(user, short_address):
    for wallet in user.wallets:
        if short_address[:6] in wallet and short_address[-4:] in wallet:
            return wallet
    return None


def process_wallet_address(bot, db, blockchain, message, waiting_for_wallet):
    wallet_address = message.text.strip()
    user_data = message.from_user
    user = db.get_user(user_data.id)
    if not user:
        bot.send_message(message.chat.id, "Ошибка: пользователь не найден.")
        return
    if len(user.wallets) >= 3:
        bot.send_message(message.chat.id, "Вы не можете добавить больше 3 кошельков.")
    elif wallet_address in user.wallets:
        bot.send_message(message.chat.id, "Этот кошелек уже добавлен.")
    else:
        db.update_user_wallet(user.user_id, wallet_address)
        short_address = wallet_address[:6] + "..." + wallet_address[-4:]
        bot.send_message(message.chat.id, f"Кошелек `{short_address}` успешно добавлен!")
    context = waiting_for_wallet.get(message.chat.id, {})
    if context.get("next_step") == "balance":
        select_wallet_for_balance(bot, db, blockchain, message)
    else:
        from BOT import send_welcome
        send_welcome(bot, message)
    del waiting_for_wallet[message.chat.id]


def select_wallet_for_balance(bot, db, blockchain, message):
    user_data = message.from_user
    user = db.get_user(user_data.id)
    if not user:
        user = models.User(user_id=user_data.id, tg_username=user_data.username or f"user_{user_data.id}")
        db.insert_user(user)
    if not user.wallets:
        handle_no_wallet_for_balance(bot, message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for wallet in user.wallets:
            short_name = wallet[:6] + "..." + wallet[-4:]
            markup.add(types.KeyboardButton(short_name))
        msg = bot.send_message(
            message.chat.id,
            "Выберите кошелек, баланс которого хотите проверить:",
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, lambda m: show_balance(bot, db, blockchain, m))


def handle_no_wallet_for_balance(bot, message):
    Keyboard.menu_not_wallet()
    bot.send_message(
        message.chat.id,
        "У вас ещё нет привязанного кошелька. Хотите добавить?",
        reply_markup=Keyboard.menu_not_wallet()
    )


def show_balance(bot, db, blockchain, message):
    if message.text == "Назад⬅️":
        bot.send_welcome(message)
        return
    user_data = message.from_user
    user = db.get_user(user_data.id)
    if not user:
        bot.send_message(message.chat.id, "Пользователь не найден.")
        return
    full_address = find_full_wallet_address(user, message.text)
    if not full_address:
        bot.send_message(
            message.chat.id,
            "Кошелёк не найден. Пожалуйста, выберите из списка.",
            reply_markup=types.ReplyKeyboardMarkup().add(types.KeyboardButton("Назад⬅️"))
        )
        return
    try:
        balance = blockchain.check_balance(full_address)
        bot.send_message(
            message.chat.id,
            f"Баланс кошелька `{full_address[:6]}...{full_address[-4:]}`: `{balance:.4f} ETH`",
            parse_mode="Markdown",
            reply_markup=types.ReplyKeyboardMarkup().add(types.KeyboardButton("Назад⬅️"))
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"Ошибка при получении баланса: {str(e)}",
            reply_markup=types.ReplyKeyboardMarkup().add(types.KeyboardButton("Назад⬅️"))
        )

def handle_transfer(bot, db, message):
    user_data = message.from_user
    user = db.get_user(user_data.id)
    if not user:
        user = models.User(user_id=user_data.id, tg_username=user_data.username or f"user_{user_data.id}")
        db.insert_user(user)

    # Всегда показываем меню, даже если нет кошельков
    bot.send_message(
        message.chat.id,
        "Выберите действие:",
        reply_markup=Keyboard.menu_transactions()
    )
