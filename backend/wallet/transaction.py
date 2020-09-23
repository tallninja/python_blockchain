import uuid
import time

from backend.wallet.wallet import Wallet

class Transaction:
    """
    Documents transfer of currency to one or more recipients
    """

    def __init__(self, sender_wallet, recipient, amount):
        self.id = str(uuid.uuid4())
        self.output = self.create_output(sender_wallet, recipient, amount)
        self.input = self.create_input(sender_wallet, self.output)

    def create_output(self, sender_wallet, recipient, amount):

        """
        Output data for the transaction
        """

        if amount > sender_wallet.balance:
            raise Exception("Amount exceeds balance")

        output = {}
        output[recipient] = amount
        output[sender_wallet.wallet_id] = sender_wallet.balance - amount

        return output

    
    def create_input(self, sender_wallet, output):
        """
        Creates the input data for the transaction
        signs the transaction data using the transaction and includes the senders public key
        """

        input = {
            "timestamp": time.time_ns(),
            "address": sender_wallet.wallet_id,
            "amount": sender_wallet.balance,
            "public_key": sender_wallet.public_key,
            "signature": sender_wallet.sign(output)
        }

        return input


    def update_transaction(self, sender_wallet, recipient, amount):
        """
        Updates a transaction to a new or existing recipient as the blocks are being mined
        """

        if amount > self.output[sender_wallet.wallet_id]: #checks if the amount we are trying to transact exceeds the account balance 
            raise Exception("Amount exceeds balance")

        if recipient in self.output: #if the recipient already exists in our previous transaction
            self.output[recipient] += amount

        else: #if it is a new recipient
            self.output[recipient] = amount

        self.output[sender_wallet.wallet_id] -= amount

        self.input = self.create_input(sender_wallet, self.output) 

    
    def to_json(self):
        """
        serialize the transaction object to a json format
        """

        return self.__dict__


    @staticmethod
    def is_valid_transaction(transaction):
        output_sum = sum(transaction.output.values())

        if transaction.input['amount'] != output_sum:
            raise Exception("Invalid transaction due to the output_sum !!!")

        if not Wallet.verify(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']
        ):

            raise Exception("Invalid transaction signature !!!")


def main():
    wallet = Wallet()
    transaction = Transaction(wallet, "foo", 15)

    print(f"Transaction: {transaction.__dict__}")


if __name__ == '__main__':
    main()

