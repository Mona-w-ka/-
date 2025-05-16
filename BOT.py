import telebot
from telebot import types
import Bchain
import Keyboard
import Wallets
from Wallets import handle_transfer
import models
from DB import Bd
from config import TOKEN, WALLET, URL, TARGET_CHAT_ID


class Bot:
    db = Bd()

    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.blockchain = Bchain.Bchain(URL, WALLET)
        self.target_chat_id = TARGET_CHAT_ID
        self.waiting_for_feedback = {}
        self.waiting_for_wallet = {}
        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_handle(message):
            self.send_welcome(message)

        @self.bot.message_handler(func=lambda message: True)
        def universal_handler(message):
            if message.text == 'Назад⬅️':
                self.send_welcome(message)
            elif message.text in ["Баланс", "Курс", "Отзыв"]:
                self.handle_button_click(message)
            elif message.text in ["BTC", "TON", "ETH"]:
                from Crypt_price import handle_currency
                handle_currency(self.bot, message)
            elif message.text == "Добавить кошелек":
                context = Wallets.ask_for_wallet_address(self.bot, message.chat.id, next_step="balance")
                self.waiting_for_wallet[message.chat.id] = context
            elif message.chat.id in self.waiting_for_wallet:
                Wallets.process_wallet_address(self.bot, self.db, self.blockchain, message, self.waiting_for_wallet)
            elif message.chat.id in self.waiting_for_feedback:
                self.process_feedback(message)
            elif message.text == "Перевод":
                handle_transfer(self.bot, self.db, message)
            elif message.text in ["Между своими", "Другому юзеру"]:
                from Wallets import on_development_message
                on_development_message(self.bot, message)

    def send_welcome(self, message):
        user_data = message.from_user
        user_id = user_data.id
        tg_username = user_data.username or f"user_{user_id}"
        user = models.User(user_id=user_id, tg_username=tg_username)
        self.db.insert_user(user)
        self.bot.send_message(
            user.user_id,
            "Привет! Что ты хочешь сделать?",
            reply_markup=Keyboard.menu_main()
        )

    def copy_message(self, message):
        try:
            user = message.from_user
            username = user.username or f"{user.first_name} {user.last_name}".strip() or f"user_{user.id}"
            text = f"📩 Отзыв от {username}:\n{message.text}"
            self.bot.send_message(chat_id=self.target_chat_id, text=text)
            return True
        except Exception as e:
            print(f"Ошибка при пересылке: {e}")
            return False

    def handle_button_click(self, message):
        if message.text == "Баланс":
            from Wallets import select_wallet_for_balance
            select_wallet_for_balance(self.bot, self.db, self.blockchain, message)
        elif message.text == "Отзыв":
            self.bot.send_message(
                message.chat.id,
                "Напишите ваш отзыв:",
                reply_markup=types.ReplyKeyboardRemove()
            )
            self.waiting_for_feedback[message.chat.id] = True
        elif message.text == "Курс":
            self.bot.send_message(
                message.chat.id,
                "Выберите криптовалюту:",
                reply_markup=Keyboard.menu_crypto()
            )
        elif message.text == "Перевод":
            from Wallets import handle_transfer
            handle_transfer(self.bot, self.db, message)
        elif message.text == "Совершить перевод":
            from Wallets import show_transaction_options
            show_transaction_options(self.bot, self.db, self.blockchain, message)

    def process_feedback(self, message):
        if self.copy_message(message):
            self.bot.send_message(
                message.chat.id,
                "✅ Ваш отзыв отправлен администраторам!",
                reply_markup=Keyboard.menu_main()
            )
        else:
            self.bot.send_message(
                message.chat.id,
                "❌ Не удалось отправить отзыв."
            )
        del self.waiting_for_feedback[message.chat.id]

    def run(self):
        print("Бот запущен!")
        self.bot.infinity_polling()


if __name__ == "__main__":
    bot = Bot(TOKEN)
    bot.run()