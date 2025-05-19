from web3 import Web3
from config import WALLET, URL
from web3.exceptions import TransactionNotFound

class Bchain:
    def __init__(self, URL, WALLET):
        self.url = URL
        self.default_wallet = WALLET
        self.web3 = Web3(Web3.HTTPProvider(URL))
        print(f"Подключение: {self.web3.is_connected()}")
        if not self.web3.is_connected():
            raise ConnectionError("Не удалось подключиться к блокчейну")

    def check_balance(self, address=None):

        wallet_address = address
        try:
            balance = self.web3.eth.get_balance(wallet_address)
            return self.web3.from_wei(balance, 'ether')
        except Exception as e:
            raise ValueError(f"Ошибка при получении баланса для {wallet_address}: {e}")


