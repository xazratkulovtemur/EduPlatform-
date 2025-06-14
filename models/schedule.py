import json
from datetime import datetime

class Schedule:
    def __init__(self, id, class_id, day):
        self.id = id
        self.class_id = class_id
        self.day = day.strip().lower()
        self.lessons = {}  # {time: {"subject": str, "teacher_id": int, "room": str}}

    def add_lesson(self, time, subject, teacher_id, room=""):
        self.lessons[time.strip()] = {
            "subject": subject.strip(),
            "teacher_id": teacher_id,
            "room": room.strip()
        }

    def remove_lesson(self, time):
        if time in self.lessons:
            del self.lessons[time]

    def get_lessons(self):
        return dict(sorted(self.lessons.items()))

    def to_dict(self):
        return {
            "id": self.id,
            "class_id": self.class_id,
            "day": self.day,
            "lessons": json.dumps(self.lessons)
        }

    @classmethod
    def from_dict(cls, data):
        schedule = cls(
            int(data["id"]),
            data["class_id"],
            data["day"]
        )
        schedule.lessons = json.loads(data.get("lessons", "{}"))
        return schedule