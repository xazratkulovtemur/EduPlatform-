
from core.user import User
from datetime import datetime

class Student(User):
    def __init__(self, _id, full_name, email, password, grade):
        super().__init__(_id, full_name, email, password, role='Student')
        self.grade = grade
        self.subjects = {}  # subject: teacher_id
        self.assignments = {}  # assignment_id: status
        self.grades = {}  # subject: [grades]

    def submit_assignment(self, assignment_id, content):
        self.assignments[assignment_id] = {"content": content, "submitted_at": datetime.now().isoformat()}

    def view_grades(self, subject=None):
        if subject:
            return self.grades.get(subject, [])
        return self.grades

    def calculate_average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0
