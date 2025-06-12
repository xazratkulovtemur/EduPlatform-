class Notification:
    def __init__(self, notif_id, message, recipient_id, created_at):
        self.id = notif_id
        self.message = message
        self.recipient_id = recipient_id
        self.created_at = created_at
        self.is_read = False

    def send(self):
        # This would normally dispatch the message
        print(f"Sent to {self.recipient_id}: {self.message}")

    def mark_as_read(self):
        self.is_read = True