from blockchain import *
from transaction import *
from wallet import *

if __name__ == '__main__':

    alice_wallet = Wallet()
    bob_wallet = Wallet()

    tx1 = Transaction(alice_wallet.get_public_key_string(), bob_wallet.get_public_key_string(), 50)
    tx1.sign_transaction(alice_wallet.private_key)

    blockchain = BlockChain()

    blockchain.add_transactions(tx1)
    blockchain.mine_pending_transactions(alice_wallet.get_public_key_string())

    for block in blockchain.chain:
        print(f"Block {block.index}")
        for tx in block.transactions:
            print(f"Sender: {tx.sender}")
            print(f"Recipient: {tx.recipient}")
            print(f"Amount: {tx.amount}")
            print(f"Signature: {tx.signature}")
    print(f"Is blockchain valid? {blockchain.is_chain_valid()}")
