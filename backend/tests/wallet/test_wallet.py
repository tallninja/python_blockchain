import pytest

from backend.wallet.wallet import Wallet

DATA = "FOO"

@pytest.fixture
def wallet():
    return Wallet()

@pytest.fixture
def signature(wallet):
    return wallet.sign(DATA)

def test_wallet(wallet):
    assert isinstance(wallet, Wallet)

def test_valid_wallet(wallet, signature):
    assert wallet.verify(wallet.public_key, DATA, signature)

def test_invalid_wallet(wallet, signature):
    assert not wallet.verify(Wallet().public_key, DATA, signature)