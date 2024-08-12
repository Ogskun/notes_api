from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User


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


class UserInfo(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE,
        related_name='user_info',
    )

    name = models.CharField(
        max_length=50, 
        null=False,
    )

    def __str__(self):
        return self.name
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_info(sender, instance=None, created=False, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)