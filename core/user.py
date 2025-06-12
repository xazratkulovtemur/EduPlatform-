from core.abstract_role import AbstractRole

class User(AbstractRole):
    def __init__(self, _id, full_name, email, password, role):
        super().__init__(_id, full_name, email, password)
        self.role = role
        self._notifications = []

    def add_notification(self, message):
        self._notifications.append({"id": len(self._notifications)+1, "message": message})

    def view_notifications(self):
        return self._notifications

    def delete_notification(self, notif_id):
        self._notifications = [n for n in self._notifications if n["id"] != notif_id]

    def get_profile(self):
        return {
            "id": self._id,
            "name": self._full_name,
            "email": self._email,
            "role": self.role
        }

    def update_profile(self, full_name=None, email=None):
        if full_name:
            self._full_name = full_name
        if email:
            self._email = email