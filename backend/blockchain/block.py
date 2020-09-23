import time
from backend.utilities.hash import Hash
from backend.utilities.hex_bin import hex_to_bin
from backend.config import MINE_RATE

GENESIS_DATA = {
    "timestamp": 1,
    "last_hash": "genesis_last_hash",
    "data": "genesis_data",
    "hash": str(Hash.hash("genesis_hash")),
    "difficulty": 3,
    "nonce": 0
}

class Block:
    """
    Block: This is a unit of storage of a transaction
    contains: data, last_hash, hash
    """

    def __init__(self, timestamp, last_hash, data, hash, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.data = data
        self.hash = hash
        self.difficulty = difficulty
        self.nonce = nonce


    def __repr__(self):
        return (
            "Block( "
            f"timestamp: {self.timestamp}, "
            f"last_hash: {self.last_hash}, "
            f"data: {self.data}, "
            f"hash: {self.hash}, "
            f"difficulty: {self.difficulty}, "
            f"nonce: {self.nonce} )"
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_block):
        """
        deserialises the json data
        """

        return Block(**json_block)


    @staticmethod
    def mine_block(last_block, data):
        """
        This is used to mine/validate our blocks
        It is responsible for doing the proof of work using the leading 0's proof of work
        """

        block_timestamp = time.time_ns()
        block_last_hash = last_block.hash
        block_data = data
        block_difficulty = Block.dynamic_difficulty(last_block, block_timestamp)
        block_nonce = 0
        block_hash = str(Hash.hash(block_timestamp, block_last_hash, block_data, block_difficulty, block_nonce))

        while hex_to_bin(block_hash)[0:block_difficulty] != '0' * block_difficulty:
            block_nonce += 1
            block_timestamp = time.time_ns()
            block_difficulty = Block.dynamic_difficulty(last_block, block_timestamp)
            block_hash = str(Hash.hash(block_timestamp, block_last_hash, block_data, block_difficulty, block_nonce))

        return Block(block_timestamp, block_last_hash, block_data, block_hash, block_difficulty, block_nonce)

    @staticmethod
    def genesis():
        return Block(**GENESIS_DATA) #unpacks the genesis data dictionary

    
    @staticmethod
    def dynamic_difficulty(last_block, new_timestamp):
        """
        Adjusts the block dificulty rate dynamically
        """

        if(new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if(last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1


    @staticmethod
    def block_validity(last_block, block):
        """
        Ensures that the block to be added meets the filloeing requirements:
            -The last hash of the block is equal to the last-block hash
            -The block meets the proof of work requirements 
            -The block's difficulty adjusts by 1
            -The block hash is the same as the result of the hashed data 
        """

        if block.last_hash != last_block.hash:
            raise Exception("The last hash is invalid !!!")

        if hex_to_bin(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception("The proof of work requirement was not met !!!")

        if abs(block.difficulty - last_block.difficulty) > 1:
            raise Exception("The block difficulty adjustment is not 1 !!!")

        hashed_data = str(Hash.hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
        ))

        if hashed_data != block.hash:
            raise Exception("The block hash is invalid !!!")


def main():
    """
    This will be executed when the block.py file is run
    """

    # genesis_block = Block.genesis()
    # block = Block.mine_block(genesis_block, "One")
    # print(block)

    last_block = Block.genesis()
    bad_block = Block.mine_block(last_block, "foo-bar")
    # bad_block.last_hash = "bad_hash"
    bad_block.difficulty = 5
    bad_block.data = "bar-foo"

    try:
        Block.block_validity(last_block, bad_block)

    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    main()