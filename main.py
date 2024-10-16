from blockchain import *

if __name__ == '__main__':

    blockchain = BlockChain()

    blockchain.add_block(Block(1,blockchain.get_last_block().hash,'Block 1 Data'))
    blockchain.add_block(Block(2,blockchain.get_last_block().hash,'Block 2 Data'))

    for block in blockchain.chain:
        print(f"Block {block.index} Block Data: {block.data} Hash: {block.hash} Nonce: {block.nonce}")

    print(f"Is the blockchain Valid? {blockchain.is_chain_valid()}")