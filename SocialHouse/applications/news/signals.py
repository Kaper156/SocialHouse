from django.db.models.signals import post_save
from django.dispatch import receiver
from applications.news.models import News

# from django.utils.text import slugify
from applications.core.utils.slug import slugify

#
# @receiver(post_save, sender=News)
# def create_news(sender, instance, **kwargs):
#     if instance.slug_url is None:
#         instance.slug_url = slugify(instance.title)
#         instance.save()
