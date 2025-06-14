import csv
from datetime import datetime
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_sample_data():
    # Sample Admins
    admins = [
        {
            "id": 0,
            "full_name": "Admin One",
            "email": "admin@edu.uz",
            "password_hash": hash_password("admin"),
            "created_at": "2025-06-14",
            "role": "ADMIN",
            "permissions": '["add_user", "remove_user", "generate_report"]'
        }
    ]

    # Sample Teachers
    teachers = [
        {
            "id": 100,
            "full_name": "John Mathematics",
            "email": "john.math@edu.uz",
            "password_hash": hash_password("teach123"),
            "created_at": "2025-06-15",
            "role": "TEACHER",
            "subjects": '["Math", "Physics"]',
            "classes": '["9-A", "10-B"]'
        },
        {
            "id": 101,
            "full_name": "Sarah Literature",
            "email": "sarah.lit@edu.uz",
            "password_hash": hash_password("teach456"),
            "created_at": "2025-06-15",
            "role": "TEACHER",
            "subjects": '["Literature", "History"]',
            "classes": '["9-B", "11-A"]'
        }
    ]

    # Sample Students
    students = [
        {
            "id": 200,
            "full_name": "Alice Johnson",
            "email": "alice@edu.uz",
            "password_hash": hash_password("student1"),
            "created_at": "2025-06-16",
            "role": "STUDENT",
            "grade": "9-A",
            "subjects": '{"Math": 100, "Physics": 100}',
            "assignments": '{"math1": "completed", "physics1": "pending"}',
            "grades": '{"Math": [5, 4, 5], "Physics": [4, 4, 3]}'
        },
        {
            "id": 201,
            "full_name": "Bob Smith",
            "email": "bob@edu.uz",
            "password_hash": hash_password("student2"),
            "created_at": "2025-06-16",
            "role": "STUDENT",
            "grade": "10-B",
            "subjects": '{"Literature": 101, "History": 101}',
            "assignments": '{"essay1": "completed", "history1": "completed"}',
            "grades": '{"Literature": [3, 4, 5], "History": [5, 5, 4]}'
        }
    ]

    # Sample Parents
    parents = [
        {
            "id": 300,
            "full_name": "Michael Johnson",
            "email": "m.johnson@email.com",
            "password_hash": hash_password("parent1"),
            "created_at": "2025-06-17",
            "role": "PARENT",
            "children": '[200]'  # Alice Johnson's ID
        },
        {
            "id": 301,
            "full_name": "Lisa Smith",
            "email": "l.smith@email.com",
            "password_hash": hash_password("parent2"),
            "created_at": "2025-06-17",
            "role": "PARENT",
            "children": '[201]'  # Bob Smith's ID
        }
    ]

    # Write to CSV files
    with open('data/admins.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=admins[0].keys())
        writer.writeheader()
        writer.writerows(admins)

    with open('data/teachers.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=teachers[0].keys())
        writer.writeheader()
        writer.writerows(teachers)

    with open('data/students.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=students[0].keys())
        writer.writeheader()
        writer.writerows(students)

    with open('data/parents.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=parents[0].keys())
        writer.writeheader()
        writer.writerows(parents)

if __name__ == "__main__":
    create_sample_data()