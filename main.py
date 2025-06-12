# main.py
from data.data_manager import DataManager
from roles.student import Student
from roles.teacher import Teacher
from roles.parent import Parent
from roles.admin import Admin
from datetime import datetime

def create_default_admin(dm):
    if not dm.get_user_by_email("admin@edu.uz"):
        admin = Admin(1, "Super Admin", "admin@edu.uz", "adminpass")
        dm.add_user(admin)
        print("✅ Default admin created.")

def login(dm):
    email = input("Email: ")
    password = input("Password: ")
    user = dm.get_user_by_email(email)
    if user and user._password_hash == user.hash_password(password):
        return user
    print("❌ Login failed.")
    return None

def admin_panel(dm, admin):
    while True:
        print("\n[ Admin Panel ]")
        print("1. Add Student\n2. Add Teacher\n3. Add Parent\n4. Logout")
        choice = input("Select: ")
        if choice == '4':
            break

        _id = len(dm.users) + 1
        name = input("Full name: ")
        email = input("Email: ")
        password = input("Password: ")

        if choice == '1':
            grade = input("Class: ")
            student = Student(_id, name, email, password, grade)
            dm.add_user(student)
            print("✅ Student added.")
        elif choice == '2':
            teacher = Teacher(_id, name, email, password)
            dm.add_user(teacher)
            print("✅ Teacher added.")
        elif choice == '3':
            parent = Parent(_id, name, email, password)
            dm.add_user(parent)
            print("✅ Parent added.")
        else:
            print("❌ Invalid choice.")

def student_menu(student):
    while True:
        print("\n[ Student Panel ]")
        print("1. View Grades\n2. Logout")
        choice = input("Select: ")
        if choice == '1':
            print("📊 Your Grades:", student.view_grades())
        elif choice == '2':
            break
        else:
            print("❌ Invalid option.")

def parent_menu(parent, dm):
    while True:
        print("\n[ Parent Panel ]")
        print("1. View Child Grades\n2. Logout")
        choice = input("Select: ")
        if choice == '1':
            for cid in parent.children:
                child = dm.get_user_by_email(cid)
                if child:
                    print(f"\nGrades for {child._full_name}: {child.view_grades()}")
        elif choice == '2':
            break
        else:
            print("❌ Invalid option.")

def teacher_menu(teacher):
    while True:
        print("\n[ Teacher Panel ]")
        print("1. View Assigned Classes\n2. Logout")
        choice = input("Select: ")
        if choice == '1':
            print("📚 Classes:", teacher.classes)
        elif choice == '2':
            break
        else:
            print("❌ Invalid option.")

def main():
    dm = DataManager()
    from roles.student import Student
    from roles.teacher import Teacher
    from roles.parent import Parent
    from roles.admin import Admin

    role_map = {
        'Student': Student,
        'Teacher': Teacher,
        'Parent': Parent,
        'Admin': Admin
    }

    dm.load_users_from_csv(role_map)
    create_default_admin(dm)

    while True:
        print("\n=== EduPlatform ===")
        print("1. Login\n2. Exit")
        option = input("Choose: ")

        if option == '1':
            user = login(dm)
            if user:
                print(f"\n✅ Welcome {user._full_name} ({user.role})")
                if user.role == 'Admin':
                    admin_panel(dm, user)
                elif user.role == 'Student':
                    student_menu(user)
                elif user.role == 'Parent':
                    parent_menu(user, dm)
                elif user.role == 'Teacher':
                    teacher_menu(user)
        elif option == '2':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid input.")

if __name__ == "__main__":
    main()
