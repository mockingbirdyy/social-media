from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    phone = models.PositiveIntegerField(null=True, blank=True)


def profile_save(sender, **kwargs):
    if kwargs['created']:
        p = Profile(user=kwargs['instance'])
        p.save()


post_save.connect(receiver=profile_save, sender=User)
