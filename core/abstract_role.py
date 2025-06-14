from abc import ABC, abstractmethod
from datetime import datetime
import hashlib

class AbstractRole(ABC):
    def __init__(self, _id: int, full_name: str, email: str, password_hash: str, is_hashed=True):
        self._id = _id
        self._full_name = full_name.strip()
        self._email = email.strip().lower()  # Normalize email
        self._password_hash = password_hash.strip() if is_hashed else self.hash_password(password_hash)
        self._created_at = datetime.now().isoformat()
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.strip().encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        return self._password_hash == self.hash_password(password)
    
    @abstractmethod
    def get_profile(self):
        pass
    
    @abstractmethod
    def update_profile(self, full_name=None, email=None, password_hash=None):
        pass