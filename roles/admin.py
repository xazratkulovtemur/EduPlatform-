from core.user import User, Role
import json
from datetime import datetime

class Admin(User):
    def __init__(self, _id, full_name, email, password_hash, created_at=None, role=Role.ADMIN, is_hashed=True):
        created_at = created_at or datetime.now().isoformat()
        super().__init__(_id, full_name, email, password_hash, role, is_hashed)
        self._created_at = created_at
        self.permissions = ["add_user", "remove_user", "generate_report"]

    def add_user(self, user, all_users):
        if user._id not in all_users:
            all_users[user._id] = user
            return f"User '{user._full_name}' added successfully."
        return "User with this ID already exists."

    def remove_user(self, user_id, all_users):
        if user_id in all_users:
            removed_user = all_users.pop(user_id)
            return f"User '{removed_user._full_name}' removed successfully."
        return "User not found."

    def generate_report(self, all_users):
        report = {
            "total_users": len(all_users),
            "by_role": {
                "Admin": 0,
                "Teacher": 0,
                "Student": 0,
                "Parent": 0
            }
        }
        for user in all_users.values():
            role_name = user.role.name.capitalize()
            if role_name in report["by_role"]:
                report["by_role"][role_name] += 1
        return report
    
    def to_dict(self):
        base = super().to_dict()
        base.update({
            "permissions": json.dumps(self.permissions),
            "created_at": self._created_at
        })
        return base

    @classmethod
    def from_dict(cls, data):
        admin = cls(
            int(data["id"]),
            data["full_name"],
            data["email"],
            data["password_hash"],
            data.get("created_at", datetime.now().isoformat()),
            is_hashed=True
        )
        admin.permissions = json.loads(data.get("permissions", "[]"))
        return admin