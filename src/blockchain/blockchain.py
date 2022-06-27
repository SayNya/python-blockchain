from src.blockchain.block import Block
from src.blockchain.transaction_pool import TransactionPool


class Blockchain:
    def __init__(self, transaction_pool: TransactionPool):
        self.transaction_pool = transaction_pool

        self.chain = [Block()]