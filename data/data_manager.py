# data/data_manager.py
import csv
import os

class DataManager:
    def __init__(self):
        self.users = []
        self.role_files = {
            'Student': 'data/students.csv',
            'Teacher': 'data/teachers.csv',
            'Parent': 'data/parents.csv',
            'Admin': 'data/admins.csv'
        }

    def add_user(self, user):
        self.users.append(user)
        self.save_user_to_csv(user)

    def save_user_to_csv(self, user):
        file_path = self.role_files[user.role]
        is_new = not os.path.exists(file_path)
        with open(file_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(['id', 'name', 'email', 'password_hash', 'role'])
            writer.writerow([user._id, user._full_name, user._email, user._password_hash, user.role])

    def load_users_from_csv(self, role_class_map):
        for role, file_path in self.role_files.items():
            if os.path.exists(file_path):
                with open(file_path, newline='') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        user = role_class_map[role](
                            int(row['id']),
                            row['name'],
                            row['email'],
                            row['password_hash'],  # Already hashed
                            role=row['role']
                        )
                        self.users.append(user)

    def get_user_by_email(self, email):
        for u in self.users:
            if u._email == email:
                return u
        return None