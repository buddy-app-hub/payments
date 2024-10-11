from enum import Enum


class TransactionType(str, Enum):
    deposit = 'deposit'
    withdraw = 'withdraw'