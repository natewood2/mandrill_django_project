from django.db import models

class MandrillEvent(models.Model):
    message_id = models.CharField(max_length=255, unique=True)
    event_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    payload = models.JSONField()

    def __str__(self):
        return f"{self.message_id} - {self.event_type}"
