from cryptography.fernet import Fernet
from hashlib import sha256
import json
from datetime import datetime, timedelta
import os

class EncryptionUtils:
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
        return sha256(data.encode()).hexdigest()
      
      
      
class KeyManager:
    KEYS_METADATA_FILE = "src/db/keys_metadata.json"

    @staticmethod
    def save_key(key: bytes, file_path: str) -> None:
        with open(file_path, "wb") as f:
            f.write(key)

    @staticmethod
    def load_key(key_version: str, metadata_file: str = KEYS_METADATA_FILE) -> bytes:
        """Load a specific key by version from metadata."""
        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
            key_info = metadata.get(key_version)
            if not key_info:
                raise ValueError(f"Key version {key_version} not found in metadata.")
            return key_info["key"].encode()
        except FileNotFoundError:
            raise ValueError("Keys metadata file not found.")

    @classmethod
    def save_keys_metadata(cls, metadata: dict) -> None:
        os.makedirs(os.path.dirname(cls.KEYS_METADATA_FILE), exist_ok=True)
        with open(cls.KEYS_METADATA_FILE, "w") as f:
            json.dump(metadata, f, indent=4)

    @classmethod
    def load_keys_metadata(cls) -> dict:
        try:
            with open(cls.KEYS_METADATA_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @classmethod
    def add_new_key(cls) -> str:
        metadata = cls.load_keys_metadata()
        new_version = f"key_{len(metadata) + 1}"
        new_key = EncryptionUtils.generate_key()
        metadata[new_version] = {
            "key": new_key.decode(),
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "usage": 0
        }
        cls.save_keys_metadata(metadata)
        return new_version

    @classmethod
    def increment_key_usage(cls, key_version: str) -> None:
        metadata = cls.load_keys_metadata()
        if key_version in metadata:
            metadata[key_version]["usage"] += 1
            cls.save_keys_metadata(metadata)

    @classmethod
    def get_key(cls, key_version: str) -> bytes:
        metadata = cls.load_keys_metadata()
        key_info = metadata.get(key_version)
        if not key_info:
            raise ValueError(f"Key version {key_version} not found.")
        return key_info["key"].encode()
      
      


class KeyRotationManager:
    @staticmethod
    def should_rotate_key(key_info: dict, days_threshold: int = 30, usage_threshold: int = 1000) -> bool:
        created_date = datetime.strptime(key_info["created"], "%Y-%m-%d %H:%M:%S")
        days_since_creation = (datetime.now() - created_date).days
        return days_since_creation >= days_threshold or key_info["usage"] >= usage_threshold

    @classmethod
    def rotate_keys(cls, days_threshold: int = 30, usage_threshold: int = 1000) -> None:
        metadata = KeyManager.load_keys_metadata()
        for key_version, key_info in metadata.items():
            if cls.should_rotate_key(key_info, days_threshold, usage_threshold):
                new_version = KeyManager.add_new_key()
                new_key = KeyManager.get_key(new_version)
                old_key = KeyManager.get_key(key_version)

                # Example: Re-encrypt all data with the new key
                print(f"Rotating {key_version} to {new_version}")
                # reencrypt_data_with_new_key(old_key, new_key)
