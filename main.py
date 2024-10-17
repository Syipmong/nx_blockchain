from blockchain import *
from transaction import *
from wallet import *
import base64


def short_public_key(public_key_str):
        return f"{public_key_str[:30]}...{public_key_str[-30:]}"

def faucet(wallet, amount, blockchain):
    reward_transaction = Transaction('System', wallet.get_public_key_string(), amount)
    blockchain.add_transactions(reward_transaction)
    blockchain.mine_pending_transactions(wallet.get_public_key_string())
    print(f"Granted {amount} units to {short_public_key(wallet.get_public_key_string())}")

if __name__ == '__main__':

    alice_wallet = Wallet()
    bob_wallet = Wallet()
    blockchain = BlockChain()

    print(f"Alice's Balance: {blockchain.get_balance(alice_wallet.get_public_key_string())}")
    print(f"Bob's Balance: {blockchain.get_balance(bob_wallet.get_public_key_string())}\n")

    faucet(alice_wallet, 100, blockchain)
    faucet(bob_wallet, 100, blockchain)
    print(f"Alice's Balance: {blockchain.get_balance(alice_wallet.get_public_key_string())}\n")
    print(f"Bob's Balance: {blockchain.get_balance(bob_wallet.get_public_key_string())}\n")

    tx1 = Transaction(alice_wallet.get_public_key_string(), bob_wallet.get_public_key_string(), 50)
    tx1.sign_transaction(alice_wallet.private_key)
    tx1.verify_transaction(alice_wallet.get_public_key_string())

    blockchain.add_transactions(tx1)
    blockchain.mine_pending_transactions(alice_wallet.get_public_key_string())

    print(f"\nBalances after Mining\n")
    print(f"Bob's Balance: {blockchain.get_balance(bob_wallet.get_public_key_string())}")
    print(f"Alice's Balance: {blockchain.get_balance(alice_wallet.get_public_key_string())}")

    tx2 = Transaction(bob_wallet.get_public_key_string(), alice_wallet.get_public_key_string(), 25)
    tx2.sign_transaction(bob_wallet.private_key)

    blockchain.add_transactions(tx2)
    blockchain.mine_pending_transactions(bob_wallet.get_public_key_string())


    print(f"\n Final Balances after Mining\n")
    print(f"Bob's Balance: {blockchain.get_balance(bob_wallet.get_public_key_string())}")
    print(f"Alice's Balance: {blockchain.get_balance(alice_wallet.get_public_key_string())}")




    for block in blockchain.chain:
        print(f"\nBlock {block.index}")
    for tx in block.transactions:
        print(f"Sender: {short_public_key(tx.sender)}")
        print(f"Recipient: {short_public_key(tx.recipient)}")
        print(f"Amount: {tx.amount}")
        if tx.signature:
            signature = base64.b64encode(tx.signature).decode('utf-8')
            print(f"Signature: {signature}")
        else:
            print("Signature: None")


    print(f"\nIs blockchain valid? {blockchain.is_chain_valid()}")

    blockchain.save_to_file('blockchain.json')

    blockchain.load_from_file('blockchain.json')


