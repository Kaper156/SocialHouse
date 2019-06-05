from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from applications.core.models import Worker


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Worker.objects.get_or_create(user=instance)

#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.worker.save()


# post_save.connect(save_user_profile, User)
