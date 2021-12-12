from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):

    """ Creates user profile model. Can be monitored using Django Admin. """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """ Returns the username of the user. """

        return self.user.username


def create_profile(
    sender,
    instance,
    created,
    **kwargs
    ):
    """  Creates user and adds to user profile model. """

    if created:
        UserProfile.objects.create(user=instance)


# Saves user profile to database

post_save.connect(create_profile, sender=User)
