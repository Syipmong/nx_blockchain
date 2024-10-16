from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class Wallet:
    def __init__(self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key().public_key()

    def sign_transaction(self, transaction):
        transaction_string = f"{transaction.sender} {transaction.recipient} {transaction.amount}".encode()

        signature = self.private_key.sign(
            transaction_string,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256)),
            hashes.SHA256()
        )
        return signature
    
    def get_public_key_string(self):
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return public_key_bytes().decode('utf-8')
    

