class Bd:
    userlist = []
    transactlist = []
    adminlist = []

    def insert_user(self, user):

        if not self.get_user(user.user_id):
            self.userlist.append(user) #добавляем пользователя
            print(f"Пользователь {user.tg_username} добавлен в БД")
        else:
            print(f"Пользователь {user.tg_username} уже существует")

    def get_user(self, user_id):

        for user in self.userlist:
            if user.user_id == user_id:
                return user
        return None

    def update_user_wallet(self, user_id, wallet_address): #добавляем кошелек пользователю

        user = self.get_user(user_id)
        if user:
            if wallet_address not in user.wallets:
                user.wallets.append(wallet_address)
                print(f"Кошелек {wallet_address} добавлен пользователю {user.tg_username}")
            else:
                print(f"Кошелек уже добавлен")
        else:
            print("Пользователь не найден")

    def add_transaction(self, transaction): #Добавляем транзакцию
        self.transactlist.append(transaction)
        print("Транзакция добавлена")