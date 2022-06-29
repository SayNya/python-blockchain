class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def add_transaction(self):
        pass

    @property
    def last_block(self):
        return self.chain[-1]
