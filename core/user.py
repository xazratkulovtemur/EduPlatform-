from core.abstract_role import AbstractRole
from enum import Enum

class Role(Enum):
    ADMIN = "Admin"
    TEACHER = "Teacher"
    STUDENT = "Student"
    PARENT = "Parent"

class User(AbstractRole):
    def __init__(self, _id: int, full_name: str, email: str, password_hash: str, role: Role, is_hashed=True):
        super().__init__(_id, full_name, email, password_hash, is_hashed)
        self.role = role
        self._notifications = []
    
    def get_profile(self):
        return {
            "id": self._id,
            "name": self._full_name,
            "email": self._email,
            "role": self.role.value,
            "created_at": self._created_at
        }
    
    def update_profile(self, full_name=None, email=None, password_hash=None):
        if full_name:
            self._full_name = full_name.strip()
        if email:
            self._email = email.strip().lower()
        if password_hash:
            self._password_hash = self.hash_password(password_hash) if not password_hash.startswith('$') else password_hash
    
    def add_notification(self, message):
        self._notifications.append({"id": len(self._notifications)+1, "message": message})

    def view_notification(self):
        return self._notifications
    
    def delete_notification(self, id):
        self._notifications=[n for n in self._notifications if n["id"]!=id]

    def to_dict(self):
        return {
            "id": self._id,
            "full_name": self._full_name,
            "email": self._email,
            "password_hash": self._password_hash,
            "created_at": self._created_at,
            "role": self.role.name
        }