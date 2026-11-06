from django.db import models


class ContactMessage(models.Model):
    """Stores incoming messages from the portfolio contact form."""
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"Message from {self.name} ({self.email}) at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

