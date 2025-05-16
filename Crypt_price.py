import Keyboard
import requests

def get_crypto_price(currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={currency}&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get(currency, {}).get('usd')
    except Exception as e:
        print(f"Ошибка получения курса: {e}")
        return None


def handle_currency(bot, message):
    currency_map = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'TON': 'the-open-network'
    }

    currency_name = message.text
    api_name = currency_map.get(currency_name)

    if api_name:
        price = get_crypto_price(api_name)
        if price:
            bot.send_message(
                message.chat.id,
                f"Текущий курс {currency_name}: ${price:.2f}",
                reply_markup=getattr(__import__('Keyboard'), 'menu_crypto')()
            )
        else:
            bot.send_message(
                message.chat.id,
                f"Не удалось получить курс {currency_name}. Попробуйте позже.",
                reply_markup=getattr(__import__('Keyboard'), 'menu_crypto')()
            )
    else:
        bot.send_message(
            message.chat.id,
            "Валюта не найдена.",
            reply_markup=getattr(__import__('Keyboard'), 'menu_crypto')()
        )