from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

class Transaction:
    def __init__(self, sender, recipient, amount, signature=""):
        self.sender = sender 
        self.recipient = recipient
        self.amount = amount
        self.signature = signature  

    def is_valid_transaction(self):
        if self.sender == "System":
            return True

        if not self.signature:
            print("Transaction has no signature")
            return False

        try:
            public_key = serialization.load_pem_public_key(self.sender.encode())
        except Exception as e:
            print(f"Failed to load public key: {e}")
            return False

        transaction_string = f"{self.sender} {self.recipient} {self.amount}".encode()

        try:
            signature_bytes = base64.b64decode(self.signature)
        except Exception as e:
            print(f"Failed to decode signature: {e}")
            return False

        try:
            public_key.verify(
                signature_bytes,
                transaction_string,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print("Transaction signature verified successfully.")
            return True
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False
