from bankaccount import BankAccount
import datetime
from abc import ABC, abstractmethod


class Transaction(ABC):

    def __init__(self, date: datetime.date, amount: float, currency: str, account_limit: float
                 ,transaction_type ,usd_allowed: bool = False, exchange_rate=float,usd_limit: bool = False):

        self._usd_limit = usd_limit
        self._exchange_rate = exchange_rate
        self._account_limit = account_limit
        self._currency = currency
        self._amount = amount
        self._date = date
        self._usd_allowed = usd_allowed

        self._nis_balance: float = 0
        self._usd_balance: float = 0

        self._transaction: dict[datetime.date: list[Transaction]] = {}
        self._transaction_type = transaction_type

    def _get_date(self):
        return self._date

    def _get_amount(self):
        return self._amount

    def _get_currency(self):
        return self._currency

    def _get_exchange_rate(self):
        return self._exchange_rate

    def _get_usd_balance(self):
        return self._usd_balance

    def _set_account_limit(self):
        return self._account_limit

    def _get_nis_balance(self):
        return self._nis_balance

    def _set_usd_allowed(self):
        return self._usd_allowed

    def _set_exchange_rate(self, new_exchange_rate: float) -> float:

        if new_exchange_rate > 0:
            self._exchange_rate = new_exchange_rate
            return new_exchange_rate

    @staticmethod
    def _valid_parameters(self,amount, currency):
        return amount > 0 and currency in ('nis', 'usd')

    def withdraw(self, amount, currency):

        if not self._valid_parameters(amount,currency):
            return False

        if self._currency == 'nis':
            if self._nis_balance - amount >= (self._account_limit * -1):
                self._nis_balance -= amount
            else:
                return False
        else:
            if self._usd_allowed and self._usd_balance >= amount:
                self._usd_balance -= amount
            else:
                return False

    def deposit(self, amount, currency ):

        if not self._valid_parameters(amount, currency):
            return False

        if self._nis_balance == 'nis':
            self._nis_balance += amount
        else:
            if not self._usd_allowed:
                return False
            else:
                self._usd_balance += amount
                return True

























#
    # def __init__(self, transaction_type: str, amount: float, currency: float, deposit: BankAccount,
    #              withdraw: BankAccount, transaction: dict):
    #
    #     self._transaction: dict[datetime.date: list[Transaction]] = {}
    #     self._withdraw = withdraw
    #     self._deposit = deposit
    #     self._currency = currency
    #     self._amount = amount
    #     self._transaction_type = transaction_type
    #
    # @staticmethod
    # def _valid_params(amount, currency):
    #     return amount > 0 and currency in ('nis', 'usd')
    #
    # # def withdraw(self,withdraw):
    # #     return BankAccount.withdraw(100)

