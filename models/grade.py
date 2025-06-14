import json
from datetime import datetime

class Grade:
    def __init__(self, id, student_id, subject, value, date=None, teacher_id=None, assignment_id=None, comment=""):
        self.id = id
        self.student_id = student_id
        self.subject = subject.strip()
        self.value = value  # 1–5
        self.date = date or datetime.now().isoformat()
        self.teacher_id = teacher_id
        self.assignment_id = assignment_id
        self.comment = comment.strip()

    def update_grade(self, value, comment=None):
        self.value = value
        if comment is not None:
            self.comment = comment.strip()
        self.date = datetime.now().isoformat()

    def get_grade_info(self):
        return {
            "grade_id": self.id,
            "student_id": self.student_id,
            "assignment_id": self.assignment_id,
            "subject": self.subject,
            "grade": self.value,
            "date": self.date,
            "teacher_id": self.teacher_id,
            "comment": self.comment
        }

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject": self.subject,
            "value": self.value,
            "date": self.date,
            "teacher_id": self.teacher_id,
            "assignment_id": self.assignment_id,
            "comment": self.comment
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            int(data["id"]),
            int(data["student_id"]),
            data["subject"],
            int(data["value"]),
            data.get("date"),
            data.get("teacher_id"),
            data.get("assignment_id"),
            data.get("comment", "")
        )