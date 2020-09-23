import pytest

from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_transaction():
    sender_wallet = Wallet()
    amount = 20
    recipient = 'recipient'
    transaction = Transaction(sender_wallet, recipient, amount)

    assert isinstance(transaction, Transaction)
    assert isinstance(sender_wallet, Wallet)

    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.wallet_id] == sender_wallet.balance - amount

    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['public_key'] == sender_wallet.public_key
    assert transaction.input['address'] == sender_wallet.wallet_id

    assert sender_wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

def test_transaction_balance():
    with pytest.raises(Exception, match="Amount exceeds balance"):
        Transaction(Wallet(), "recipient", 1000000000)
    


def test_transaction_update_balance():
    sender_wallet = Wallet()
    recipient = "recipient"
    amount = 100
    transaction = Transaction(sender_wallet, recipient, amount)

    with pytest.raises(Exception, match="Amount exceeds balance"):
        transaction.update_transaction(sender_wallet, recipient, 1000000)


def test_transaction_update_existing_recipient():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 100
    transaction = Transaction(sender_wallet, recipient, amount)
    new_amount = 100
    transaction.update_transaction(sender_wallet, recipient, new_amount)

    assert transaction.output[recipient] == amount + new_amount
    assert transaction.output[sender_wallet.wallet_id] == sender_wallet.balance - (amount + new_amount)
    assert sender_wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def test_transaction_update_new_recipient():
    sender_wallet = Wallet()
    recipient = "recipient"
    amount = 100
    transaction = Transaction(sender_wallet, recipient, amount)

    new_recipient = 'new_recipient'
    new_amount = 50
    transaction.update_transaction(sender_wallet, new_recipient, new_amount)

    assert transaction.output[sender_wallet.wallet_id] == sender_wallet.balance - (amount + new_amount)
    assert transaction.output[new_recipient] == new_amount 
    assert sender_wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def test_is_valid_transaction():
    Transaction.is_valid_transaction(Transaction(Wallet(), 'recipient', 100))

def test_valid_transaction_altered_account_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 100)

    transaction.output[sender_wallet.wallet_id] = 100000

    with pytest.raises(Exception, match="Invalid transaction due to the output_sum !!!"):
        transaction.is_valid_transaction(transaction)


def test_is_valid_transaction_altered_signature():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 100)

    transaction.input['signature'] = Wallet().sign(transaction.output)

    with pytest.raises(Exception, match="Invalid transaction signature !!!"):
        transaction.is_valid_transaction(transaction)
