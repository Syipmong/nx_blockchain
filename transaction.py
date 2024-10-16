from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = None

    def sign_transaction(self, private_key):
        transaction_string = f"{self.sender} {self.recipient} {self.amount}".encode()
        self.signature = private_key.sign(
            transaction_string,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Transaction signed successfully.")

    def verify_transaction(self, public_key_str):
        if self.sender == 'System':
            return True

        if not self.signature:
            print("No signature in the transaction")
            return False

        transaction_string = f"{self.sender} {self.recipient} {self.amount}".encode()
        public_key = serialization.load_pem_public_key(public_key_str.encode())
        try:
            public_key.verify(
                self.signature,
                transaction_string,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print("Signature verification successful.")
            return True
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False
