from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes, serialization
import base64

class Transaction:
    def __init__(self, sender, recipient, amount, signature=None, fee=1):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature
        self.fee = fee

    def get_total_amount(self):
        return self.amount + self.fee


    def sign_transaction(self, private_key):
        transaction_string = f"{self.sender} {self.recipient} {self.amount} {self.fee}".encode()
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

        transaction_string = f"{self.sender} {self.recipient} {self.amount} {self.fee}".encode()
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

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'fee': self.fee,
            'signature': base64.b64encode(self.signature).decode('utf-8') if self.signature else None
        }

    @staticmethod
    def from_dict(data):
        signature = base64.b64decode(data['signature']) if data['signature'] else None
        return Transaction(data['sender'], data['recipient'], data['amount'], signature)
    
    
    

    
