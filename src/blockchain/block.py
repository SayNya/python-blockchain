from hashlib import sha256


class Block:
    def __init__(self, data, timestamp):
        self.timestamp = timestamp
        self.data = data
        self.hash = self.get_hash()
        self.prevHash = None

    def get_hash(self):
        block_hash = sha256()
        # block_hash.update(str(self.prevHash).encode('utf-8'))
        block_hash.update(str(self.timestamp).encode('utf-8'))
        block_hash.update(str(self.data).encode('utf-8'))
        return block_hash.hexdigest()
