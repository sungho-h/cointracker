"""
Given a list of withdrawals and desposits, detect the likely transfers amongst them.

[
	('tx_id_1', 'wallet_id_1', '2020-01-01 15:30:20 UTC', 'out', 5.3),  # 5.3 BTC was withdrawn out of 'wallet_id_1'
	('tx_id_2', 'wallet_id_1', '2020-01-03 12:05:25 UTC', 'out', 3.2),  # 3.2 BTC was withdrawn out of 'wallet_id_1'
	('tx_id_3', 'wallet_id_2', '2020-01-01 15:30:20 UTC', 'in', 5.3),   # 5.3 BTC was deposited into 'wallet_id_2'
	('tx_id_4', 'wallet_id_3', '2020-01-01 15:30:20 UTC', 'in', 5.3),   # 5.3 BTC was deposited into 'wallet_id_3'
]

Expected output:
[
	('tx_id_1', 'tx_id_3'),
]

My implementation of Transactions has id, wallet_address, balnce_change, time, and hash.
"in" and "out" will be determined by the balance_change being positive and negative

assumption 1. if transactions are ordered by time, 'out' will occur at or before 'in'
assumption 2. time between 'out' and 'in' is maxed at 5 min
"""
from collections import deque, defaultdict
from datetime import datetime
import unittest

def detect_transfers(transactions):
    detected = []
    fuzzyness_time_diff = 300 # 300sec -> 5min
    cache = defaultdict(lambda: deque())
    for transaction in sorted(transactions, key=lambda x: x.time):
        balance_change = transaction.balance_change
        if balance_change < 0:
            cache[-balance_change].append(transaction)
        else:
            if len(cache[balance_change]) < 1:
                continue
            for prev_transaction in cache[balance_change]:
                # if current transaction and prev_transaction has more than 5 min diff remove from deque
                curr_time = datetime.strptime(transaction.time, '%Y-%m-%d %H:%M:%S')
                prev_time = datetime.strptime(prev_transaction.time, '%Y-%m-%d %H:%M:%S')
                if ((curr_time-prev_time).total_seconds() > fuzzyness_time_diff):
                    print("removed due to fuzzy time diff")
                    cache[balance_change].remove(prev_transaction)
                if transaction.wallet_address == prev_transaction.wallet_address:
                    continue
                detected.append((prev_transaction.id, transaction.id))
                cache[balance_change].remove(prev_transaction)
                break
    return detected

class Transaction:
    def __init__(self, id, wallet_address, balance_change, time, hash) -> None:
        self.id = id
        self.wallet_address = wallet_address
        self.balance_change = balance_change
        self.time = time
        self.hash = hash


class DetectTransfersTestCase(unittest.TestCase):

    def test_base(self):
        self.assertEqual(detect_transfers([]),[])

    def test_base(self):
        test_case = []
        test_case.append(Transaction('tx_id_1', 'wallet_id_1', -5.3, '2020-01-01 15:30:20', 'tmp_hash'))
        test_case.append(Transaction('tx_id_2', 'wallet_id_1', -3.2, '2020-01-03 12:05:25', 'tmp_hash'))
        test_case.append(Transaction('tx_id_3', 'wallet_id_2', 5.3, '2020-01-01 15:30:20', 'tmp_hash'))
        test_case.append(Transaction('tx_id_4', 'wallet_id_3', 5.3, '2020-01-01 15:30:20', 'tmp_hash'))
        self.assertEqual(detect_transfers(test_case),[('tx_id_1', 'tx_id_3')])


if __name__ == '__main__':
    unittest.main()