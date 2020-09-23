import time

from backend.blockchain.block import Block
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback


PUBLISH_KEY = "pub-c-9945ed65-7b19-42c8-860b-c5a3bb0a63d2"
SUBSCRIBE_KEY = "sub-c-cbe6e2f6-aa37-11ea-baa3-a65cc700836a"
CHANNELS = {
    "FOO": "FOO",
    "BLOCK": "BLOCK"
}

pnconfig = PNConfiguration()
pnconfig.publish_key = PUBLISH_KEY
pnconfig.subscribe_key = SUBSCRIBE_KEY


class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubsub, message):
        print(f"Channel: {message.channel}\nMessage: {message.message}\n\n")

        if message.channel == CHANNELS["BLOCK"]:
            new_block = Block.from_json(message.message)
            potential_chain = self.blockchain.chain[:]

            potential_chain.append(new_block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print("The new block has been added successfully\n")

            except Exception as e:
                print(f"Failed to add new block !!!:\nError: {e}\n")





class PubSub:
    """
    Handles publishung data to our channels
    """

    def __init__(self, blockchain):
        self.pubsub = PubNub(pnconfig)
        self.pubsub.subscribe().channels(CHANNELS.values()).execute()
        self.pubsub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        """
        Publish a message to the channel
        """
        self.pubsub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a mined block to other channels on the pubsub network
        """

        self.publish(CHANNELS['BLOCK'], block.to_json())


def main():
    pubsub = PubSub()
    time.sleep(2)
    pubsub.publish(CHANNELS['FOO'], "Hello world !")
    

if __name__ == '__main__':
    main()