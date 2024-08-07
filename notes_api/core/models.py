from django.conf import settings
from django.db import models
from django.utils import timezone


class Note(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=100,
        blank=False, 
        null=False,
    )

    content = models.TextField()
    is_deleted = models.BooleanField(
        default=False,
    )

    date_created = models.DateField(
        auto_now_add=True,
    )
    
    def __str__(self):
        return self.title