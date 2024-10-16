from blockchain import *
from transaction import *
from wallet import *
import base64

if __name__ == '__main__':

    alice_wallet = Wallet()
    bob_wallet = Wallet()

    tx1 = Transaction(alice_wallet.get_public_key_string(), bob_wallet.get_public_key_string(), 50)
    tx1.sign_transaction(alice_wallet.private_key)

    blockchain = BlockChain()

    blockchain.add_transactions(tx1)
    blockchain.mine_pending_transactions(alice_wallet.get_public_key_string())  # Alice is rewarded for mining

    for block in blockchain.chain:
        print(f"\nBlock {block.index}")
        for tx in block.transactions:
            print(f"Sender: {tx.sender}")
            print(f"Recipient: {tx.recipient}")
            print(f"Amount: {tx.amount}")
            if tx.signature:
                signature = base64.b64encode(tx.signature).decode('utf-8')
                print(f"Signature: {signature}")
            else:
                print("Signature: None")

    print(f"\nIs blockchain valid? {blockchain.is_chain_valid()}")

    blockchain.save_to_file('blockchain.json')

    blockchain.load_from_file('blockchain.json')