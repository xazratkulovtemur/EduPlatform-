from data.data_manager import DataManager
import hashlib
import os
from core.user import Role
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(data_manager):
    
    print("\nLogin to EduPlatform")
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    user = data_manager.authenticate_user(email, password)
    
    if user:
        
        print(f"\nWelcome, {user._full_name} ({user.role.name})!")
        return user
    
    print("\nLogin failed. Invalid email or password.")
    input("Press Enter to continue...")
    return None

def admin_menu(admin, data_manager):
    while True:
        
        print(f"\nAdmin Panel: {admin._full_name}")
        print("1. Add user")
        print("2. Remove user")
        print("3. View all users")
        print("4. Logout")

        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            
            print("\nAdd New User")
            role = input("Role (admin/teacher/student/parent): ").lower().strip()
            
            try:
                _id = int(input("ID: "))
                full_name = input("Full name: ").strip()
                email = input("Email: ").strip().lower()
                password = input("Password: ")
                created_at = input("Created at (ISO format or leave empty for now): ").strip() or datetime.now().isoformat()

                if role == "admin":
                    from roles.admin import Admin
                    user = Admin(_id, full_name, email, password, created_at)
                elif role == "teacher":
                    from roles.teacher import Teacher
                    user = Teacher(_id, full_name, email, password, created_at)
                elif role == "student":
                    from roles.student import Student
                    grade = input("Grade (e.g., 9-A): ").strip()
                    user = Student(_id, full_name, email, password, created_at, grade)
                elif role == "parent":
                    from roles.parent import Parent
                    user = Parent(_id, full_name, email, password, created_at)
                else:
                    print("Invalid role.")
                    input("Press Enter to continue...")
                    continue

                if data_manager.add_user(admin._id, user):
                    data_manager.save_all()
                
            except ValueError:
                print("Invalid ID. Must be a number.")
            
            input("Press Enter to continue...")

        elif choice == "2":
            
            print("\nRemove User")
            try:
                user_id = int(input("Enter user ID to remove: "))
                if data_manager.remove_user(admin._id, user_id):
                    data_manager.save_all()
            except ValueError:
                print("Invalid ID. Must be a number.")
            input("Press Enter to continue...")

        elif choice == "3":
            
            print("\nAll Users")
            all_users = data_manager.get_all_users()
            for user in all_users:
                print(f"ID: {user._id}, Name: {user._full_name}, Role: {user.role.name}, Email: {user._email}")
            input("\nPress Enter to continue...")

        elif choice == "4":
            break

def teacher_menu(teacher, data_manager):
    while True:
        
        print(f"\nTeacher Panel: {teacher._full_name}")
        print("1. Create assignment")
        print("2. Grade assignment")
        print("3. View student progress")
        print("4. Logout")

        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            print("\nCreating assignment...")
            # Implementation would go here
            input("Press Enter to continue...")
        
        elif choice == "4":
            break

def student_menu(student, data_manager):
    while True:
        
        print(f"\nStudent Panel: {student._full_name}")
        print("1. Submit assignment")
        print("2. View grades")
        print("3. Logout")

        choice = input("\nSelect option: ").strip()
        
        if choice == "3":
            break

def parent_menu(parent, data_manager):
    while True:
        
        print(f"\nParent Panel: {parent._full_name}")
        print("1. View child grades")
        print("2. View child assignments")
        print("3. View child notifications")
        print("4. Logout")

        choice = input("\nSelect option: ").strip()
        
        if choice == "4":
            break

if __name__ == "__main__":
    dm = DataManager()
    dm.load_all()

    while True:
        
        print("\nEduPlatform Management System")
        print("1. Login")
        print("2. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            user = login(dm)
            if user:
                if user.role == Role.ADMIN:
                    admin_menu(user, dm)
                elif user.role == Role.TEACHER:
                    teacher_menu(user, dm)
                elif user.role == Role.STUDENT:
                    student_menu(user, dm)
                elif user.role == Role.PARENT:
                    parent_menu(user, dm)
        
        elif choice == "2":
            print("\nSaving data...")
            dm.save_all()
            print("Exiting EduPlatform. Goodbye!")
            break