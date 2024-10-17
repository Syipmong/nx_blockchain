from transaction import Transaction
import json
from block import Block

class BlockChain:
    def __init__(self):
        self.difficulty = 5
        self.chain = [self.create_first_block()]
        self.pending_transactions = []
        self.mining_reward = 100

    def create_first_block(self):
        first_block = Block(0, '0', [], self.difficulty)
        first_block.mine_block()
        return first_block

    def add_transactions(self, transaction):
        if transaction.sender != "System":
            sender_balance = self.get_balance(transaction.sender)
            if sender_balance < transaction.amount:
                print("Insufficient balance. Transaction rejected!")
                return
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

    def save_to_file(self, filename='blockchain.json'):
        try:
            with open(filename, 'w') as file:
                # json.dump([block.to_dict() for block in self.chain], file)
                json.dump(self.chain, file, default=lambda x: x.to_dict())
            print("Blockchain saved successfully.")
        except Exception as e:
            print(f"Error saving blockchain: {e}")

    def load_from_file(self, filename='blockchain.json'):
        try:
            with open(filename, 'r') as file:
                chain_data = json.load(file)
                self.chain = [Block.from_dict(block_data) for block_data in chain_data]
            print("Blockchain loaded successfully.")
        except FileNotFoundError:
            print("No existing blockchain found. Creating a new one.")
        except Exception as e:
            print(f"Error loading blockchain: {e}")

    def get_balance(self, public_key_str):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == public_key_str:
                    balance -= tx.amount
                if tx.recipient == public_key_str:
                    balance += tx.amount

        return balance
