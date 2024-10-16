import hashlib
import time
import base64
from transaction import Transaction

class Block:
    def __init__(self, index, previous_hash, transactions, difficulty=5):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = time.time()
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        transaction_string = "".join([str(tx.to_dict()) for tx in self.transactions])
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.nonce}{transaction_string}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        while self.hash[:self.difficulty] != '0' * self.difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block Mined: {self.hash}")

    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'difficulty': self.difficulty,
            'hash': self.hash
        }

    @staticmethod
    def from_dict(data):
        transactions = [Transaction.from_dict(tx_data) for tx_data in data['transactions']]
        block = Block(data['index'], data['previous_hash'], transactions, data['difficulty'])
        block.timestamp = data['timestamp']
        block.nonce = data['nonce']
        block.hash = data['hash']
        return block
