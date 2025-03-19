from django.db import models
from users.models import User

class Notification(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(null=True, blank=True) 

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Action logged for {self.user} at {self.created_at}"
