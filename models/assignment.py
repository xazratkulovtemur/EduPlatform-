import json
from datetime import datetime

class Assignment:
    def __init__(self, id, title, description, deadline, subject, teacher_id, class_id, difficulty="medium"):
        self.id = id
        self.title = title.strip()
        self.description = description.strip()
        self.deadline = deadline  # ISO format string
        self.subject = subject.strip()
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.difficulty = difficulty.lower()
        self.submissions = {}  # {student_id: content}
        self.grades = {}       # {student_id: grade}

    def add_submission(self, student_id, content):
        self.submissions[student_id] = {
            "content": content.strip(),
            "submitted_at": datetime.now().isoformat(),
            "status": "submitted"
        }

    def set_grade(self, student_id, grade):
        if student_id in self.submissions:
            self.grades[student_id] = {
                "value": grade,
                "graded_at": datetime.now().isoformat(),
                "teacher_id": self.teacher_id
            }

    def get_status(self):
        return {
            "total_students": len(self.submissions),
            "submitted": list(self.submissions.keys()),
            "graded": list(self.grades.keys())
        }

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "subject": self.subject,
            "teacher_id": self.teacher_id,
            "class_id": self.class_id,
            "difficulty": self.difficulty,
            "submissions": json.dumps(self.submissions),
            "grades": json.dumps(self.grades)
        }

    @classmethod
    def from_dict(cls, data):
        assignment = cls(
            int(data["id"]),
            data["title"],
            data["description"],
            data["deadline"],
            data["subject"],
            int(data["teacher_id"]),
            data["class_id"],
            data.get("difficulty", "medium")
        )
        assignment.submissions = json.loads(data.get("submissions", "{}"))
        assignment.grades = json.loads(data.get("grades", "{}"))
        return assignment