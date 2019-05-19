from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime


class Person(models.Model):
    name = models.CharField(max_length=128, blank=True, verbose_name="Имя")
    patronymic = models.CharField(max_length=128, blank=True, verbose_name="Отчество")
    surname = models.CharField(max_length=256, blank=True, verbose_name="Фамилия")

    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    positions = models.ManyToManyField('Position', through='PersonPosition', related_name='Persons')

    def FIO(self, full=False):
        if not full:
            return f"{self.name[0]}.{self.patronymic[0]}. {self.surname}"
        return f"{self.name} {self.patronymic} {self.surname}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.person.save()


post_save.connect(save_user_profile, User)


class Position(models.Model):
    title = models.CharField(max_length=128, verbose_name="Название должности")
    purpose = models.TextField(max_length=1024, verbose_name="Назначение должности", blank=True)


class PersonPosition(models.Model):
    position = models.ForeignKey('Position', related_name='membership', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', related_name='membership', on_delete=models.CASCADE)
    date_of_appointment = models.DateField(verbose_name="Дата устройства на должность",
                                           default=datetime.datetime.now)
    dismissal_date = models.DateField(verbose_name="Дата увольнения с должности", null=True)
