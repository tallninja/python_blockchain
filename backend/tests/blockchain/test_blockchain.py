import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA

@pytest.fixture
def blockchain():
    return Blockchain()


@pytest.fixture
def foo_chain(blockchain):
    for i in range(3):
        blockchain.add_block(i)

    return blockchain


def test_blockchain(blockchain):
    assert blockchain.chain[0].hash == GENESIS_DATA["hash"] 


def test_add_block(blockchain):
    data = "foo"
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data


def test_blockchain_vlidity(blockchain, foo_chain):
    blockchain.blockchain_validity(foo_chain.chain)


def test_bad_genesis_block(blockchain, foo_chain):
    foo_chain.chain[0].data = "foo"

    with pytest.raises(Exception, match="The chain does not begin with the genesis block !!!"):
        blockchain.blockchain_validity(foo_chain.chain)


def test_replace_chain(foo_chain):
    blockchain = Blockchain()
    blockchain.replace_chain(foo_chain.chain)

    assert blockchain.chain == foo_chain.chain

def test_replace_chain_shorter_chain(foo_chain):
    blockchain = Blockchain()
    
    with pytest.raises(Exception, match="The chain must be longer than the existing chain !!!"):
        foo_chain.replace_chain(blockchain.chain)

def test_replace_chain_bad_chain(foo_chain):
    blockchain = Blockchain()
    foo_chain.chain[1].data = "foo"

    with pytest.raises(Exception, match="The chain is invalid:"):
        blockchain.replace_chain(foo_chain.chain)


