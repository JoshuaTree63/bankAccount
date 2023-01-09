from bankaccount import BankAccount


class Person:

    def __init__(self, person_id: str, name: str, address: str, phone: str):

        self._phone = phone
        self._address = address
        self._name = name
        self._person_id = person_id