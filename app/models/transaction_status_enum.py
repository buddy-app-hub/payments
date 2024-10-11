from enum import Enum


class TransactionStatus(str, Enum):
    approved = 'approved'
    pending = 'pending'
    canceled = 'canceled'