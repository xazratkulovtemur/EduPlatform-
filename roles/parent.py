from core.user import User, Role
import json
from datetime import datetime

class Parent(User):
    def __init__(self, _id, full_name, email, password_hash, created_at=None, role=Role.PARENT, is_hashed=True):
        created_at = created_at or datetime.now().isoformat()
        super().__init__(_id, full_name, email, password_hash, role, is_hashed)
        self._created_at = created_at
        self.children = []

    def view_child_grades(self, child_id, all_students):
        student = all_students.get(child_id)
        if student:
            return student.view_grades()
        return "Student not found."

    def view_child_assignments(self, child_id, all_students):
        student = all_students.get(child_id)
        if student:
            return student.assignments
        return "Student not found."

    def receive_child_notification(self, child_id, all_students):
        student = all_students.get(child_id)
        if student:
            return student.view_notification()
        return "Student not found."

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "children": json.dumps(self.children),
            "created_at": self._created_at
        })
        return base

    @classmethod
    def from_dict(cls, data):
        parent = cls(
            int(data["id"]),
            data["full_name"],
            data["email"],
            data["password_hash"],
            data.get("created_at", datetime.now().isoformat()),
            is_hashed=True
        )
        parent.children = json.loads(data.get("children", "[]"))
        return parent