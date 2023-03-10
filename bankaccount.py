import datetime
from transaction import *
from person import Person


class BankAccount:

    def __init__(self, bank_name: str, branch: str, account_num: int, holders: set[Person]
                 , usd_allowed: bool = False, credit_limit: float = 0,):

        self._credit_limit = credit_limit
        self._holder: set[Person] = holders
        self._account_num = account_num
        self._branch = branch
        self._bank_name = bank_name

        self._nis_balance: float = 0
        self._usd_balance: float = 0
        self._usd_allowed: bool = usd_allowed
        self.nis_credit_limit: float = 0

    def __str__(self):
        return f"Account { self._account_num}"

    @staticmethod
    def _valid_params(amount, currency):
        return amount > 0 and currency in ('nis', 'usd')

    def _add_transaction(self, transaction_type: str, amount: float, currency: str):
        transaction_date = datetime.date.today()

        if transaction_date not in self._transaction:
            self._transaction[transaction_date] = []

        self._transaction[transaction_date].append(Transaction(transaction_type,amount, currency))

    def withdraw(self, amount: float, currency: str = 'nis') -> bool:

        if not self._valid_params(amount, currency):
            return False

        if currency == 'nis':
            if self._nis_balance - amount >= (self.nis_credit_limit * -1):
                self._nis_balance -= amount
            else:
                return False
        else:
            if self._usd_allowed and self._usd_balance >= amount:
                self._usd_balance -= amount
            else:
                return False

        self._add_transaction('withdraw', amount=amount, currency=currency)
        return True

    def deposit(self, amount: float, currency: str = 'nis'):

        if not self._valid_params(amount, currency):
            return False

        if currency == 'nis':
            self._nis_balance += amount
            self._add_transaction('deposit', amount, currency)
            return True
        else:
            if not self._usd_allowed:
                return False
            else:
                self._add_transaction('deposit', amount=amount, currency=currency)
                self._usd_balance += amount
                return True

    def convert_to_usd(self, nis_amount: float, nis2usd_exchange_rate: float) -> bool:

        if nis_amount <= 0:
            return False
        if not self._usd_allowed or self._nis_balance - nis_amount < (self.nis_credit_limit* -1):
            return False
        self._nis_balance -= nis_amount
        self._usd_balance += nis_amount*nis2usd_exchange_rate
        self._add_transaction('convert to usd',amount= nis_amount,currency='nis')
        return True

    def convert_to_nis(self, usd_amount: float, usd2nis_exchange_rate: float) -> bool:

        if usd_amount < 0:
            return False

        if not self._usd_allowed or self._usd_balance< usd_amount:
            return False
        self._nis_balance = usd_amount*usd2nis_exchange_rate
        self._usd_balance -= usd_amount
        self._add_transaction("exchange to nis", amount=usd_amount, currency='usd')
        return True

    def get_current_balance(self) -> tuple[float,float]:
        return self._nis_balance, self._usd_balance

    def get_transactions_per_date(self, date: datetime.date) -> list[Transaction]:
        return self._transaction.get(date,[])


if __name__ == '__main__':
    # create bank account
    account1 = BankAccount('Discount', 'Kiryat Hasharon', 12345,
                           set([Person('123456789', 'Valeria', 'Netanya', '054-444-4444')]),
                           usd_allowed=True, credit_limit=10_000)
    print(f"Current balance for {account1}: {account1.get_current_balance()}")

    print("Trying to withdraw 10500 shekels passing the limit - should fail!")
    result = account1.withdraw(10500)
    print(f"Result: {result}")

    print("Trying to withdraw 9500 shekels in the range of limit - should succeed!")
    result = account1.withdraw(9500)
    print(f"Result: {result}")

    print(f"Current balance: {account1.get_current_balance()}")

    print("Trying to convert 1000 shekels to USD - outside the limit, should fail")
    result = account1.convert_to_usd(1000, 3.5)
    print(f"Result: {result}")

    print("Deposit 20_000 to account - should succeed")
    result = account1.deposit(20000)
    print(f"Result: {result}")

    print("Deposit $5_000 to account - should succeed")
    result = account1.deposit(5000, currency='usd')
    print(f"Result: {result}")

    print(f"New balance: {account1.get_current_balance()}")
    print(f"Transactions: {account1.get_transactions_per_date(datetime.date.today())}")












