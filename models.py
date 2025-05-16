from datetime import datetime

class User:
    def __init__(self, user_id, tg_username, wallets=None, transactions=None, count_transaction=0):
        self.user_id = user_id
        self.tg_username = tg_username
        self.wallets = wallets if wallets is not None else []
        self.transactions = transactions if transactions is not None else []
        self.count_transaction = count_transaction


class Admin:
    def __init__(self, admin_key, tg_username):
        self.admin_key = admin_key
        self.tg_username = tg_username
        self.data_login = datetime.now()  # дата первого входа админа
        self.last_login = datetime.now()  # дата последнего входа админа


class Transaction:
    def __init__(self, reqvits_reciver, reqvisits_sender, user_id, error="", status="pending"):
        self.time_start = datetime.now()
        self.time_end = None
        self.error = error
        self.status = status
        self.reqvits_reciver = reqvits_reciver
        self.reqvisits_sender = reqvisits_sender
        self.user_id = user_id