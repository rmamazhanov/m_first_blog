# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
from medical_app.models import Department, Schedules


class Profile(models.Model):
    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    inn = models.CharField(max_length=14, verbose_name='ИНН', null=True)
    card_id = models.IntegerField(verbose_name='Номер карточки', null=True)
    middle_name = models.CharField(max_length=255, verbose_name='Отчество', null=True)
    birthday = models.DateField(max_length=255, verbose_name='Дата рождения', null=True)
    assigned = models.BooleanField(verbose_name='Подтвержден', default=False)
    sex = models.IntegerField(verbose_name='Пол', null=True)
    department_id = models.ForeignKey(Department, to_field='department_id', null=True, verbose_name='Отделение')
    hospital = models.ForeignKey('medical_app.Hospital', verbose_name='Госпиталь', null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Appointment(models.Model):
    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    appointment_id = models.CharField(verbose_name='ID записи', null=False, max_length=255)
    profile = models.ForeignKey(Profile)
    schedule = models.ForeignKey(Schedules)