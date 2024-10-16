import hashlib
import time
from transaction import Transaction
import json
import os

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


class BlockChain:
    def __init__(self):
        self.difficulty = 4
        self.chain = [self.create_first_block()]
        self.pending_transactions = []
        self.mining_reward = 100

    def create_first_block(self):
        first_block = Block(0, '0', [], self.difficulty)
        first_block.mine_block()
        return first_block

    def add_transactions(self, transaction):
        if transaction.verify_transaction(transaction.sender):
            self.pending_transactions.append(transaction)
            print("Transaction added successfully.")
        else:
            print("Invalid Transaction. Transaction rejected!")

    def mine_pending_transactions(self, miner_address):
        reward_transaction = Transaction('System', miner_address, self.mining_reward)
        self.pending_transactions.append(reward_transaction)
        new_block = Block(len(self.chain), self.get_last_block().hash, self.pending_transactions, self.difficulty)
        new_block.mine_block()
        self.chain.append(new_block)
        self.pending_transactions = []

    def get_last_block(self):
        return self.chain[-1]

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def save_to_file(self, filename):
        try:
            with open(filename, '+w') as file:
                json.dump([block.to_dict() for block in self.chain], file)
            print("Blockchain saved successfully.")
        except Exception as e:
            print(f"Error saving blockchain: {e}")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.chain = [Block.from_dict(block_data) for block_data in json.load(file)]
            print("Blockchain loaded successfully.")
        except FileNotFoundError:
            print("No existing blockchain found. Creating a new one.")
        except Exception as e:
            print(f"Error loading blockchain: {e}")