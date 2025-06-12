from core.user import User

class Parent(User):
    def __init__(self, _id, full_name, email, password):
        super().__init__(_id, full_name, email, password, role='Parent')
        self.children = []  # list of student IDs

    def view_child_grades(self, child):
        return child.view_grades()

    def view_child_assignments(self, child):
        return child.assignments

    def receive_child_notification(self, child):
        return child.view_notifications()