from cryptography.fernet import Fernet
import base64
import os

# Generate a key (store this securely)
SECRET_KEY = base64.urlsafe_b64encode(os.urandom(32))
cipher = Fernet(SECRET_KEY)

def encrypt_data(data):
    if not data:
        return None
    return cipher.encrypt(data.encode()).decode()  # Convert bytes to string

def decrypt_data(encrypted_data):
    if not encrypted_data:
        return None
    return cipher.decrypt(encrypted_data.encode()).decode()  # Convert string back to bytes
