import hashlib
import time
import json

class Block:
    def __init__(self, index, previous_hash, data, timestamp):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp

        # Serialize data to JSON if it's not the genesis block
        if index == 0:
            self.data = data  # Genesis block contains plain text
        else:
            self.data = json.dumps(data)  # Serialize data to JSON string

        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculate the hash of the block using its attributes.
        """
        block_string = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def get_data(self):
        """
        Deserialize the data back to a dictionary (or return as-is for the genesis block).
        """
        if self.index == 0:
            return self.data  # Return genesis block data as-is
        return json.loads(self.data)  # Deserialize JSON data


class Blockchain:
    def __init__(self, name):
        """
        Initialize a new blockchain with a genesis block.
        """
        self.name = name
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """
        Create the first block in the blockchain (genesis block).
        """
        return Block(0, "0", f"Genesis Block for {self.name}", time.time())

    def get_latest_block(self):
        """
        Get the most recent block in the blockchain.
        """
        return self.chain[-1]

    def add_block(self, data):
        """
        Add a new block to the blockchain.
        """
        new_block = Block(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            data=data,
            timestamp=time.time()
        )
        self.chain.append(new_block)

    def add_transplant(self, donor_data, recipient_data):
        """
        Add a transplant record to the blockchain.
        """
        data = {
            "donor": donor_data,
            "recipient": recipient_data,
            "timestamp": time.time()
        }
        self.add_block(data)

    def get_all_blocks(self):
        """
        Get all blocks in the blockchain.
        """
        return self.chain

    def search_blocks(self, search_term):
        """
        Search for blocks containing the given search term in their data.
        """
        results = []
        for block in self.chain:
            if search_term.lower() in str(block.data).lower():
                results.append(block)
        return results

    def print_chain(self):
        """
        Print all blocks in the blockchain (for debugging).
        """
        print(f"--- {self.name} Chain ---")
        for block in self.chain:
            print(f"Block {block.index} [Hash: {block.hash}, Previous Hash: {block.previous_hash}, Data: {block.data}]")