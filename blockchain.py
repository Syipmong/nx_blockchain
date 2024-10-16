import hashlib
import time

from transaction import *

class Block:
    def __init__(self, index, previous_hash, data, transactions, difficulty=4):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.transactions = transactions
        self.timestamp = time.time()
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        transaction_string = "".join([str(tx.__dict__) for tx in self.transactions])
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.nonce}{transaction_string}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        while self.hash[:self.difficulty] != '0' * self.difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block Mined: {self.hash}")


class BlockChain:
    def __init__(self):
        self.difficulty = 4
        self.chain = [self.create_first_block()]
        self.pending_transactions = []
        self.mining_reward = 100

    def create_first_block(self):
        first_block = Block(0, '0', 'First Block', [], self.difficulty)
        first_block.mine_block()
        return first_block

    def add_transaction(self, transaction):
        if transaction.is_valid_transaction():
            self.pending_transactions.append(transaction)
        else:
            print("Invalid Transaction. Transaction rejected!")

    def mine_pending_transactions(self, miner_address):
        reward_transaction = Transaction('System', miner_address, self.mining_reward)
        self.pending_transactions.append(reward_transaction)

        new_block = Block(len(self.chain), self.get_last_block().hash, 'Pending Transactions', self.pending_transactions, self.difficulty)
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
                print("Current block hash is invalid!")
                return False

            if current_block.previous_hash != previous_block.hash:
                print("Previous block hash is invalid!")
                return False

            for transaction in current_block.transactions:
                if not transaction.is_valid_transaction():
                    print("Invalid transaction in block!")
                    return False

        return True
