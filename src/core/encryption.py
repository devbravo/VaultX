from cryptography.fernet import Fernet 
from hashlib import sha256


class EncryptionManager:
  """
  A utility class to manage encryption, decryption and hashing operations. 
  """
  @staticmethod
  def generate_key() -> bytes:
      return Fernet.generate_key()
    
  @staticmethod     
  def encrypt_data(key: bytes, data: str) -> bytes:
    f = Fernet(key) 
    return f.encrypt(data.encode())
  
  @staticmethod
  def decrypt_data(key: bytes, encrypted_data: bytes) -> str: 
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()
  
  @staticmethod
  def hash_data(data: str) -> str:
      """Hash data using SHA-256."""
      return sha256(data.encode()).hexdigest()
    
  @staticmethod
  def rotate_key(old_key: bytes, new_key: bytes, encrypted_data: bytes) -> bytes: 
    f_old = Fernet(old_key) 
    f_new = Fernet(new_key) 
    decrypted_data = f_old.decrypt(encrypted_data) 
    return f_new.encrypt(decrypted_data)
  
  @staticmethod
  def save_key(key: bytes, file_path: str) -> None:
      with open(file_path, "wb") as f:
          f.write(key)

  @staticmethod
  def load_key(file_path: str) -> bytes:
      with open(file_path, "rb") as f:
          return f.read()

