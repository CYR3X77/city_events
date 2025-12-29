from django.db import models
from django.contrib.auth.models import User
from events.models import Event


class Review(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='reviews'   # 👈 ВОТ ОНО
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f'{self.user.username} — {self.event.title}'
