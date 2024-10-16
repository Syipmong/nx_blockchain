from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
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
        public_key = serialization.load_pem_public_key(self.sender.encode())
        transaction_string = f"{self.sender} {self.recipient} {self.amount}"

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
            return True
        except:
            return False

    