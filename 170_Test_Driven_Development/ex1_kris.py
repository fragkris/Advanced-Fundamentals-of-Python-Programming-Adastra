class Account:

    def __init__(self, acc_number: str, date_open: str, interest_rate: float, opening_balance: float) -> None:
        self.accNumber = acc_number
        self.dateOpen = date_open
        self.interestRate = interest_rate
        self.opening_balance = opening_balance

    def deposit(self, amount):
        pass

    def withdraw(self, amount):
        pass

    def transfer(self, to_acc_number, amount):
        pass
