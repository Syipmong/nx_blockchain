from blockchain import *
from transaction import *

if __name__ == '__main__':

    blockchain = BlockChain()

    blockchain.add_transactions(Transaction('Yipmong', 'Said', 30))
    blockchain.add_transactions(Transaction('Said', 'Yipmong', 20))
    blockchain.add_transactions(Transaction('John', 'Said', 10))
    blockchain.add_transactions(Transaction('Nelson', 'Hosiah', 5))

    print('Mining new block ...')

    blockchain.mine_pending_transactions('Yipmong')

    for block in blockchain.chain:
        print(f"Block {block.index}:")
        for tx in block.transactions:
            print(f"{tx.sender} sent {tx.amount} to {tx.recipient}")

    print(f"Is the BlockChain Valid? {blockchain.is_chain_valid()}")