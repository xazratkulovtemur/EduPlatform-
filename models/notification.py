import json
from datetime import datetime
from enum import Enum, auto

class Priority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

class Notification:
    def __init__(self, id, message, recipient_id, created_at=None, priority=Priority.MEDIUM, is_read=False):
        self.id = id
        self.message = message.strip()
        self.recipient_id = recipient_id
        self.created_at = created_at or datetime.now().isoformat()
        self.priority = priority if isinstance(priority, Priority) else Priority[priority]
        self.is_read = is_read

    def mark_as_read(self):
        self.is_read = True

    def send(self):
        self.is_read = False
        return f"Notification sent to {self.recipient_id} at {self.created_at}"

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "recipient_id": self.recipient_id,
            "created_at": self.created_at,
            "priority": self.priority.name,
            "is_read": self.is_read
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            int(data["id"]),
            data["message"],
            int(data["recipient_id"]),
            data.get("created_at"),
            Priority[data.get("priority", "MEDIUM")],
            data.get("is_read", False)
        )