""" Key Rotation Management Module

This module provides utilities for managing the lifecycle of encryption keys by monitoring their age and usage. 
It ensures compliance with security best practices by implementing key rotation policies and supporting re-encryption of data with newly generated keys.
"""

from datetime import datetime
from src.core.encryption import KeyManager
import logging

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
                logging.info(f"Rotating key: {key_version} -> {new_version}")
                return old_key, new_key, new_version