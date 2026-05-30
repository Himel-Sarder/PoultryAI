from django.db import models
from accounts.models import User


class Notification(models.Model):
    TYPE_CHOICES = [
        ('order', 'Order'),
        ('message', 'Message'),
        ('system', 'System'),
        ('social', 'Social'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='system')
    link = models.CharField(max_length=300, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.full_name}"
