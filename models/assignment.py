class Assignment:
    def __init__(self, assignment_id, title, description, deadline, subject, teacher_id, class_id):
        self.id = assignment_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.subject = subject
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.submissions = {}  # student_id: content
        self.grades = {}  # student_id: grade

    def add_submission(self, student_id, content):
        self.submissions[student_id] = content

    def set_grade(self, student_id, grade):
        self.grades[student_id] = grade

    def get_status(self):
        return {
            "submitted": len(self.submissions),
            "graded": len(self.grades)
        }