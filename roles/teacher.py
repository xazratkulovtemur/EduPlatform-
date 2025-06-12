from core.user import User

class Teacher(User):
    def __init__(self, _id, full_name, email, password):
        super().__init__(_id, full_name, email, password, role='Teacher')
        self.subjects = []
        self.classes = []
        self.assignments = {}  # assignment_id: Assignment

    def create_assignment(self, assignment_id, title, description, deadline, subject, class_id):
        self.assignments[assignment_id] = {
            "title": title,
            "description": description,
            "deadline": deadline,
            "subject": subject,
            "class_id": class_id
        }

    def grade_assignment(self, assignment_id, student_id, grade):
        if assignment_id in self.assignments:
            if "grades" not in self.assignments[assignment_id]:
                self.assignments[assignment_id]["grades"] = {}
            self.assignments[assignment_id]["grades"][student_id] = grade

    def view_student_progress(self, student):
        return student.view_grades()