# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.


class Hospital(models.Model):
    class Meta:
        verbose_name = 'Госпиталь'
        verbose_name_plural = 'Госпитали'

    hospital_id = models.IntegerField(verbose_name='Госпиталь ID', unique=True)
    name = models.CharField(max_length=255, verbose_name='Название госпиталя')
    api = models.ForeignKey('base_data_app.ParserAPI', null=True, blank='API сервер')

    def __str__(self):
        return self.name


class Department(models.Model):
    class Meta:
        verbose_name = 'Отделение'
        verbose_name_plural = 'Отделения'

    department_id = models.IntegerField(verbose_name='ID Отделения', unique=True)
    name = models.CharField(max_length=255, verbose_name='Название отделения')
    hospital = models.ForeignKey(Hospital, to_field='hospital_id', verbose_name='Госпиталь', null=True)


    def __str__(self):
        return self.name


# class DoctorPosition(models.Model):
#     class Meta:
#         verbose_name = 'Специальность'
#         verbose_name_plural = 'Специальности'
#
#     position = models.CharField(max_length=255, verbose_name='Название Специальности')


class Doctor(models.Model):
    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Докторы'

    doc_id = models.IntegerField(verbose_name='ID МИС доктора', unique=True)
    image = models.ImageField(upload_to='image/doctors', verbose_name='Изображение', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='ФИО', null=True, blank=True)
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    fist_name = models.CharField(max_length=255, verbose_name='Имя')
    middle_name = models.CharField(max_length=255, verbose_name='Отчество', null=True, blank=True)
    position = models.CharField(max_length=255, verbose_name='Специальность')
    department = models.ForeignKey(Department, to_field='department_id', verbose_name='Отделение')
    resume = RichTextUploadingField(verbose_name='Образование и опыт', blank=True, null=True)

    def save(self, *agrs, **kwargs):
        self.name = str(self.last_name) + ' ' + str(self.fist_name) + ' ' + str(self.middle_name)
        super(Doctor, self).save(*agrs, **kwargs)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return "%s %s %s" % (self.last_name, self.fist_name, self.middle_name)

    def get_schedules(self):
        return self.schedules_set.all


class MedicalService(models.Model):
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    med_id = models.IntegerField(verbose_name='ID МИС услуги', unique=True)
    name = models.CharField(max_length=255, verbose_name='Название услуги')
    price = models.IntegerField(verbose_name='Стоимость')

    def __str__(self):
        return self.name


class Cabinet(models.Model):
    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'

    cabinet_id = models.IntegerField(verbose_name='ID МИС кабинета', unique=True)
    name = models.CharField(max_length=255, verbose_name='Номер или название кабинета')

    def __str__(self):
        return self.name


class Specification(models.Model):
    class Meta:
        verbose_name = 'Спецификация'
        verbose_name_plural = 'Спецификации'

    title = models.CharField(max_length=255, verbose_name='Спецификация')
    medical_service = models.ForeignKey(MedicalService, to_field='med_id', verbose_name='Услуга')
    doctor = models.ForeignKey(Doctor, to_field='doc_id', verbose_name='Доктор')
    cabinet = models.CharField(max_length=255, verbose_name='Кабинет')

    def save(self, *agrs, **kwargs):
        self.title = str(self.medical_service.name) + ' - ' + str(self.doctor.name)
        super(Specification, self).save(*agrs, **kwargs)

    def __str__(self):
        return self.title


class Date(models.Model):
    class Meta:
        verbose_name = 'Дата'
        verbose_name_plural = 'Даты'

    dates = models.DateField(verbose_name='Дата', unique=True)

    def __str__(self):
        return str(self.dates)


class Schedules(models.Model):
    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'Графики работы'

    cab_id = models.IntegerField(verbose_name='ID Кабинета')
    doc_id = models.ForeignKey(Doctor, to_field='doc_id', verbose_name='ID Досктора')
    date = models.ForeignKey(Date, to_field='dates', verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    busy = models.BooleanField(verbose_name='Занято', default=True)


    # def __str__(self):
    #     name = str(self.cab_id) + ' ' + str(self.doc_id) + ' ' + str(self.date) + ' ' + str(self.time)
    #     return name