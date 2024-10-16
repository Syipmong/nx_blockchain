from blockchain import *
from transaction import *
from wallet import *
if __name__ == "__main__":
    # Create wallets for Alice and Bob
    alice_wallet = Wallet()
    bob_wallet = Wallet()

    # Create a transaction from Alice to Bob
    tx1 = Transaction(alice_wallet.get_public_key_string(), bob_wallet.get_public_key_string(), 50)
    tx1.signature = alice_wallet.sign_transaction(tx1)

    # Ensure the signature is correctly applied
    if tx1.signature:
        print("Transaction signed successfully.")
    else:
        print("Transaction signing failed.")

    # Create a blockchain instance
    blockchain = BlockChain()

    # Add the transaction and mine the block
    blockchain.add_transaction(tx1)
    blockchain.mine_pending_transactions(alice_wallet.get_public_key_string())

    # Print the blockchain data
    for block in blockchain.chain:
        print(f"Block {block.index}:")
        for tx in block.transactions:
            print(f"Sender: {tx.sender}\nRecipient: {tx.recipient}\nAmount: {tx.amount}")
            print(f"Signature: {tx.signature}\n")

    # Check if the blockchain is valid
    print(f"Is blockchain valid? {blockchain.is_chain_valid()}")
