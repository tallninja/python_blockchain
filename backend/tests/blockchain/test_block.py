import time
import pytest

from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, TIME_S
from backend.utilities.hex_bin import hex_to_bin


def test_mine_block():
    last_block = Block.genesis()
    data = "foo"
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_bin(block.hash)[0:block.difficulty] == '0' * block.difficulty


def test_genesis():
    genesis_block = Block.genesis()

    for key, value in GENESIS_DATA.items():
        assert getattr(genesis_block, key) == value


def test_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis(), "foo")
    mined_block = Block.mine_block(last_block, "bar")

    assert mined_block.difficulty == last_block.difficulty + 1
    

def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), "foo")
    time.sleep(MINE_RATE / TIME_S)
    mined_block = Block.mine_block(last_block, "bar")

    assert mined_block.difficulty == last_block.difficulty - 1


def test_mining_rate_1():
    last_block = Block(time.time_ns(), "last_hash", "foo", "hash", 1, 0)
    time.sleep(MINE_RATE / TIME_S)
    mined_block = Block.mine_block(last_block, "bar")

    assert mined_block.difficulty == 1

@pytest.fixture
def last_block():
    return Block.genesis()

@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, "foo_bar")


def test_valid_block(last_block, block):
    Block.block_validity(last_block, block)


def test_valid_last_hash(last_block, block):
    block.last_hash = "foo bar"

    with pytest.raises(Exception, match="The last hash is invalid !!!"):
        Block.block_validity(last_block, block)

def test_proof_of_work(last_block, block):
    block.hash = 'aabbccdd'

    with pytest.raises(Exception, match="The proof of work requirement was not met !!!"):
        Block.block_validity(last_block, block)

def test_difficulty_interval(last_block, block):
    block.difficulty = 10
    block.hash = "0000000000000000000000000aabbccdd"

    with pytest.raises(Exception, match="The block difficulty adjustment is not 1 !!!"):
        Block.block_validity(last_block, block)


def test_hash_validity(last_block, block):
    block.hash = '0000000000000000000000000aabbccdd'

    with pytest.raises(Exception, match="The block hash is invalid !!!"):
        Block.block_validity(last_block, block)


