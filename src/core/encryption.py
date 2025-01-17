from cryptography.fernet import Fernet 
from hashlib import sha256

def generate_key():
    key = Fernet.generate_key()
    return key
        
def encrypt_data(key, data):
  f = Fernet(key) 
  return f.encrypt(data.encode())

def decrypt_data(key, encrypted_data): 
  f = Fernet(key)
  return f.decrypt(encrypted_data).decode()



def hash_data(data):
    """Hash data using SHA-256."""
    return sha256(data.encode()).hexdigest()

