import uuid
import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec #Elliptic cryptography
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

from backend.config import STARTING_BALANCE

class Wallet():
    """
    Contains an individual's transaction details i.e:
        - Wallet ID
        - Balance
        - Private_key
        - Public_key
    """

    def __init__(self):
        self.wallet_id = str(uuid.uuid4())
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(), #Standards for Efficient Cryptograpy Prime (256bits) Koblitz version 1
            default_backend()
        ) #This method generates a private public key pair
        self.public_key = self.private_key.public_key()
        self.stringify_public_key()


    def sign(self, data):
        """
        Used to sign the transaction data using the individual's private key
        """

        return self.private_key.sign(
            json.dumps(data).encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )

    
    def stringify_public_key(self):
        """
        serialize the public key to a json format
        """

        self.public_key_bytes = self.public_key.public_bytes(
            encoding =serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        decoded_public_key = self.public_key_bytes.decode('utf-8')
        self.public_key = decoded_public_key
       

    @staticmethod
    def verify(public_key, data, signature):
        """
        Used to verify the wallet data
        """

        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )

        try:
            deserialized_public_key.verify(
                signature,
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
            
        except InvalidSignature:
            return False


def main():
    wallet = Wallet()
    data = "foo"
    signature = wallet.sign(data)
    public_key = wallet.public_key

    print(f"\nwallet: {wallet.__dict__}")
    print(f"\nsignature: {signature}")
    valid = wallet.verify(public_key, data, signature)
    print(f"\nvalid: {valid}")
    valid = wallet.verify(Wallet().public_key, data, signature)
    print(f"\nvalid: {valid}")

if __name__ == '__main__':
    main()
    