import csv
import json
import hashlib
import os
from datetime import datetime
from roles.admin import Admin
from roles.teacher import Teacher
from roles.student import Student
from roles.parent import Parent
from core.user import Role

class DataManager:
    def __init__(self):
        self.admins = []
        self.teachers = []
        self.students = []
        self.parents = []
        self._initialize_data_directory()

    def _initialize_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs("data", exist_ok=True)
        
        # Initialize all required CSV files
        self._initialize_csv_file("admins.csv", [
            "id", "full_name", "email", "password_hash", 
            "created_at", "role", "permissions"
        ])
        self._initialize_csv_file("teachers.csv", [
            "id", "full_name", "email", "password_hash",
            "created_at", "role", "subjects", "classes"
        ])
        self._initialize_csv_file("students.csv", [
            "id", "full_name", "email", "password_hash",
            "created_at", "role", "grade", "subjects",
            "assignments", "grades"
        ])
        self._initialize_csv_file("parents.csv", [
            "id", "full_name", "email", "password_hash",
            "created_at", "role", "children"
        ])

    def _initialize_csv_file(self, filename, fieldnames):
        """Create CSV file with headers if it doesn't exist"""
        filepath = os.path.join("data", filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.strip().encode()).hexdigest()

    def load_all(self):
        """Load all user data from CSV files"""
        self.admins = self._load_users("admins.csv", "admin")
        self.teachers = self._load_users("teachers.csv", "teacher")
        self.students = self._load_users("students.csv", "student")
        self.parents = self._load_users("parents.csv", "parent")
        
        # Create default admin if none exists
        if not self.admins:
            self._create_default_admin()

    def _load_users(self, filename, role_class):
        """Load users from a specific CSV file"""
        users = []
        filepath = os.path.join("data", filename)
        
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        user = self._create_user_from_row(row, role_class)
                        if user:
                            users.append(user)
                    except Exception as e:
                        print(f"Error loading user from {filename}: {e}")
        except FileNotFoundError:
            print(f"{filename} not found - will be created when saving")
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            
        return users

    def _create_user_from_row(self, row, role_class):
        """Create appropriate user object from CSV row"""
        if role_class == "admin":
            return Admin.from_dict(row)
        elif role_class == "teacher":
            return Teacher.from_dict(row)
        elif role_class == "student":
            return Student.from_dict(row)
        elif role_class == "parent":
            return Parent.from_dict(row)
        return None

    def _create_default_admin(self):
        """Create a default admin account if none exists"""
        default_admin = Admin(
            _id=0,
            full_name="System Admin",
            email="admin@edu.uz",
            password_hash=self.hash_password("admin"),
            created_at=datetime.now().isoformat(),
            is_hashed=True
        )
        self.admins.append(default_admin)
        self.save_all()
        print("Created default admin account")

    def save_all(self):
        """Save all user data to CSV files"""
        self._save_users(self.admins, "admins.csv")
        self._save_users(self.teachers, "teachers.csv")
        self._save_users(self.students, "students.csv")
        self._save_users(self.parents, "parents.csv")

    def _save_users(self, users, filename):
        """Save users to a specific CSV file"""
        if not users:
            return
            
        filepath = os.path.join("data", filename)
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                if users:
                    writer = csv.DictWriter(file, fieldnames=users[0].to_dict().keys())
                    writer.writeheader()
                    for user in users:
                        writer.writerow(user.to_dict())
        except Exception as e:
            print(f"Error saving to {filename}: {e}")

    def authenticate_user(self, email, password):
        """Authenticate user with email and password"""
        email = email.strip().lower()
        password_hash = self.hash_password(password)
        
        for user in self.get_all_users():
            if (user._email.lower() == email and 
                user._password_hash == password_hash):
                return user
        return None

    def get_user_by_id(self, user_id):
        """Get user by ID regardless of role"""
        for user in self.get_all_users():
            if user._id == user_id:
                return user
        return None

    def get_user_by_email(self, email):
        """Get user by email (case-insensitive)"""
        email = email.strip().lower()
        for user in self.get_all_users():
            if user._email.lower() == email:
                return user
        return None

    def get_all_users(self):
        """Get all users from all roles"""
        return self.admins + self.teachers + self.students + self.parents

    def is_admin(self, user_id):
        """Check if user is an admin"""
        user = self.get_user_by_id(user_id)
        return user and user.role == Role.ADMIN

    def add_user(self, creator_id, user):
        """Add a new user (admin only)"""
        if not self.is_admin(creator_id):
            return False, "Only admins can add users"
            
        if self.get_user_by_id(user._id):
            return False, "User ID already exists"
            
        if self.get_user_by_email(user._email):
            return False, "Email already in use"

        # Ensure password is hashed
        if not getattr(user, '_is_hashed', False):
            user._password_hash = self.hash_password(user._password_hash)
            user._is_hashed = True

        if isinstance(user, Admin):
            self.admins.append(user)
        elif isinstance(user, Teacher):
            self.teachers.append(user)
        elif isinstance(user, Student):
            self.students.append(user)
        elif isinstance(user, Parent):
            self.parents.append(user)
        else:
            return False, "Invalid user role"
            
        self.save_all()
        return True, f"User {user._full_name} added successfully"

    def remove_user(self, remover_id, user_id):
        """Remove a user (admin only)"""
        if not self.is_admin(remover_id):
            return False, "Only admins can remove users"
            
        for user_list in [self.admins, self.teachers, self.students, self.parents]:
            for user in user_list:
                if user._id == user_id:
                    user_list.remove(user)
                    self.save_all()
                    return True, f"User {user._full_name} removed"
                    
        return False, "User not found"