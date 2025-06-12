class Schedule:
    def __init__(self, schedule_id, class_id, day):
        self.id = schedule_id
        self.class_id = class_id
        self.day = day
        self.lessons = {}  # time: {"subject": str, "teacher_id": int}

    def add_lesson(self, time, subject, teacher_id):
        self.lessons[time] = {"subject": subject, "teacher_id": teacher_id}

    def view_schedule(self):
        return self.lessons

    def remove_lesson(self, time):
        if time in self.lessons:
            del self.lessons[time]