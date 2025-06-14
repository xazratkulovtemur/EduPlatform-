from core.user import User, Role
import json
from datetime import datetime

class Teacher(User):
    def __init__(self, _id, full_name, email, password_hash, created_at=None, role=Role.TEACHER, is_hashed=True):
        created_at = created_at or datetime.now().isoformat()
        super().__init__(_id, full_name, email, password_hash, role, is_hashed)
        self._created_at = created_at
        self.subjects = []
        self.classes = []
        self.assignments = {}

    def create_assignment(self, assignment_id, title, description, deadline, subject, class_id):
        self.assignments[assignment_id] = {
            "title": title,
            "description": description,
            "deadline": deadline,
            "subject": subject,
            "class_id": class_id,
            "submissions": {}
        }

    def grade_assignment(self, assignment_id, student_id, grade):
        if assignment_id in self.assignments:
            submissions = self.assignments[assignment_id]["submissions"]
            if student_id in submissions:
                submissions[student_id]["grade"] = grade

    def view_student_progress(self, student_id):
        progress = {}
        for aid, assignment in self.assignments.items():
            if student_id in assignment["submissions"]:
                submission = assignment["submissions"][student_id]
                progress[aid] = {
                    "title": assignment["title"],
                    "submitted": True,
                    "grade": submission.get("grade")
                }
        return progress
    
    def to_dict(self):
        base = super().to_dict()
        base.update({
            "subjects": json.dumps(self.subjects),
            "classes": json.dumps(self.classes),
            "created_at": self._created_at
        })
        return base

    @classmethod
    def from_dict(cls, data):
        teacher = cls(
            int(data["id"]),
            data["full_name"],
            data["email"],
            data["password_hash"],
            data.get("created_at", datetime.now().isoformat()),
            is_hashed=True
        )
        teacher.subjects = json.loads(data.get("subjects", "[]"))
        teacher.classes = json.loads(data.get("classes", "[]"))
        return teacher