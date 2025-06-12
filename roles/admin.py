from core.user import User

class Admin(User):
    def __init__(self, _id, full_name, email, password):
        super().__init__(_id, full_name, email, password, role='Admin')
        self.permissions = []

    def add_user(self, user, user_list):
        user_list.append(user)

    def remove_user(self, user_id, user_list):
        user_list[:] = [u for u in user_list if u._id != user_id]

    def generate_report(self, users):
        return [u.get_profile() for u in users]