from backend.blockchain.block import Block

class Blockchain:
    """
    Blockchain: This is a decentralized ledger of transactions
    made up of a series of blocks connected to each other 
    """

    def __init__(self):
        genesis_block = Block.genesis()
        self.chain = [genesis_block]

    def add_block(self, data):
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block, data))

    def __repr__(self):
        return f"Chain: {self.chain}"


    def replace_chain(self, chain):
        """
        Replaces the existing chain with an incoming chain as long as the incoming chain meets the following requirements 
            - The incoming chain must be longer than the existing chain
            - The incoming chain must be valid
        """

        if len(chain) < len(self.chain):
            raise Exception("The chain must be longer than the existing chain !!!")

        try:
            Blockchain.blockchain_validity(chain)

        except Exception as e:
            raise Exception(f"The chain is invalid: {e}")

        self.chain = chain


    def to_json(self):

        # serialized_data = []
        
        # for block in self.chain:
        #     serialized_data.append(block.to_json())

        # return serialized_data

        return list(map(lambda block: block.to_json(), self.chain))


    def from_json(json_chain):
        """
        deserialises the json data
        """
        return list(map(lambda block: Block.from_json(block), json_chain))

    @staticmethod
    def blockchain_validity(chain):
        """
        Tests the validity of the blockchain using the following rules
            - The blockchain must begin with the genesis block
            - The blockchain must be formatted correctly
        """
        if chain[0] != Block.genesis():
            raise Exception("The chain does not begin with the genesis block !!!")

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.block_validity(last_block, block)

    

            


def main():
    """
    This will be executed when the blockchin file is run
    """

    chain = Blockchain()
    chain.add_block("One")
    chain.add_block("Two")

    print(chain)

if __name__ == "__main__":
    main()