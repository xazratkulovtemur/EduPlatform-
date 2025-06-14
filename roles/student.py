from core.user import User, Role
import json
from datetime import datetime

class Student(User):
    def __init__(self, _id, full_name, email, password_hash, created_at=None, grade=None, role=Role.STUDENT, is_hashed=True):
        created_at = created_at or datetime.now().isoformat()
        super().__init__(_id, full_name, email, password_hash, role, is_hashed)
        self._created_at = created_at
        self.grade = grade
        self.subjects = {}
        self.assignments = {}
        self.grades = {}

    def submit_assignment(self, assignment_id, content):
        self.assignments[assignment_id] = {
            "status": "submitted",
            "content": content
        }

    def view_grades(self, subject=None):
        if subject:
            return {subject: self.grades.get(subject, [])}
        return self.grades

    def calculate_average_grade(self):
        total = 0
        count = 0
        for grade_list in self.grades.values():
            total += sum(grade_list)
            count += len(grade_list)
        return total / count if count > 0 else 0
    
    def to_dict(self):
        base = super().to_dict()
        base.update({
            "grade": self.grade,
            "subjects": json.dumps(self.subjects),
            "assignments": json.dumps(self.assignments),
            "grades": json.dumps(self.grades),
            "created_at": self._created_at
        })
        return base

    @classmethod
    def from_dict(cls, data):
        student = cls(
            int(data["id"]),
            data["full_name"],
            data["email"],
            data["password_hash"],
            data.get("created_at", datetime.now().isoformat()),
            data["grade"],
            is_hashed=True
        )
        student.subjects = json.loads(data.get("subjects", "{}"))
        student.assignments = json.loads(data.get("assignments", "{}"))
        student.grades = json.loads(data.get("grades", "{}"))
        return student