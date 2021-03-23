# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import threading

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
# Create your views here.
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, FormView, ListView
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from zeep.plugins import HistoryPlugin
from zeep.transports import Transport
import dateutil.parser

from base_data_app.models import Contacts, Ads, News, Slider, Partners, Reviews, ParserAPI
from base_data_app.utils import get_client
from main import settings
from medical_app.models import MedicalService, Doctor, Date, Schedules, Department, Specification, Hospital
from users.forms import UserRegistrationForm
from users.models import User, Profile, Appointment
from users.views import send_email_notification


def general_params(request):
    contact = Contacts.objects.first()
    params = {
        'contact': contact,

    }

    return params


def index(request):
    services = MedicalService.objects.all()
    positions = Doctor.objects.all().distinct()[:12]
    ads = Ads.objects.all().order_by('-date')[:2]
    news = News.objects.last()
    slider = Slider.objects.all()
    partners = Partners.objects.all()[:8]
    context = {
        'services': services,
        'positions': positions,
        'ads': ads,
        'news': news,
        'slider': slider,
        'partners': partners

    }

    context.update(general_params(request))
    return render(request, 'app/index.html', context)


def news(request):
    objects = News.objects.all().order_by('-date')

    context = {
        'news': objects
    }
    context.update(general_params(request))
    return render(request, 'app/news.html', context)


def news_inner(request, id=None):
    object = News.objects.get(id=id)

    context = {
        'object': object
    }
    context.update(general_params(request))
    return render(request, 'app/news_inner.html', context)


def ads(request):
    objects = Ads.objects.all().order_by('-date')

    context = {
        'ads': objects
    }

    context.update(general_params(request))
    return render(request, 'app/ads.html', context)


def ads_inner(request, id=None):
    object = Ads.objects.get(id=id)

    context = {
        'object': object
    }

    context.update(general_params(request))
    return render(request, 'app/ads_inner.html', context)


def specialist(request):
    user = request.user
    hospital = request.GET.get('hospital')

    if user.is_authenticated():
        filters = dict(
            department_id=user.profile.department_id
        )
        if (hospital):
            filters['department__hospital__hospital_id'] = hospital
        doctor_list = Doctor.objects.filter(**filters)
    else:
        doctor_list = Doctor.objects.filter(
            department__hospital__hospital_id=hospital) if hospital else Doctor.objects.all()

    paginator = Paginator(doctor_list, 9)
    page = request.GET.get('page')
    try:
        doctors = paginator.page(page)
    except PageNotAnInteger:
        doctors = paginator.page(1)
    except EmptyPage:
        doctors = paginator.page(paginator.num_pages)

    context = {
        'doctors': doctors,
        'hospitals': Hospital.objects.all(),
        'hospital_id': hospital
    }

    context.update(general_params(request))
    return render(request, 'app/specialists_list.html', context)


def medical_services(request):
    services = MedicalService.objects.all()

    context = {
        'services': services,
    }

    context.update(general_params(request))
    return render(request, 'app/services_list.html', context)


# class DoctorDetail(DetailView):
#     model = Doctor
#     template_name = 'app/specialist.html'
def doctor_detail(request, pk):
    doc = Doctor.objects.get(id=pk)
    reviews_count = Reviews.objects.filter(doctor=doc).count()

    return render(request, 'app/specialist.html', {
        'object': doc,
        'reviews_count': reviews_count,
        'services_count': Specification.objects.filter(doctor_id=pk).count()
    })


@csrf_exempt
def doctor_schedule(request, pk=None):
    if request.method == 'POST' and request.is_ajax() and request.POST.get('next_week', '0') == '1':
        template = 'partials/specialist_schedule_items.html'
        today_date = datetime.date.today() + datetime.timedelta(7)
    else:
        template = 'app/specialist_schedule.html' if not request.is_ajax() else 'partials/specialist_schedule_items.html'
        today_date = datetime.date.today()

    start_week = today_date - datetime.timedelta(today_date.weekday())
    end_week = start_week + datetime.timedelta(6)
    doctor = Doctor.objects.get(id=pk)
    days = Date.objects.filter(dates__range=[start_week, end_week])

    context = {
        'object': doctor,
        'days': days,
        'start': start_week,
        'end': end_week,
        'reviews_count': Reviews.objects.filter(doctor_id=pk).count(),
        'services_count': Specification.objects.filter(doctor_id=pk).count()
    }

    return render(request, template, context)


def doctor_reviews(request, pk):
    doc = Doctor.objects.get(pk=pk)
    reviews = Reviews.objects.filter(doctor=doc)
    services_count = Specification.objects.filter(doctor=doc).count()
    print(doc)
    return render(request, 'app/specialist_reviews.html', {
        'object': doc,
        'reviews': reviews,
        'reviews_count': reviews.count(),
        'services_count': services_count
    })


# class DoctorServices(DetailView):
#     model = Doctor
#     template_name = 'app/specialist_services.html'


def doctor_service(request, pk):
    doc = Doctor.objects.get(id=pk)
    med_service = Specification.objects.filter(doctor=doc)
    reviews_count = Reviews.objects.filter(doctor=doc).count()

    return render(request, 'app/specialist_services.html', {
        'object': doc,
        'med_service': med_service,
        'reviews_count': reviews_count,
        'services_count': med_service.count()
    })


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid:
            form.username = request.POST.get('username')
            form.inn = request.POST.get('inn')
            if not form.inn:
                form.inn = '0'
            form.last_name = request.POST.get('last_name')
            form.first_name = request.POST.get('first_name')
            form.middle_name = request.POST.get('middle_name')
            form.birthday = request.POST.get('birthday')
            form.email = request.POST.get('email')
            form.password1 = request.POST.get('password1')
            form.password2 = request.POST.get('password2')
            form.hospital = request.POST.get('hospital')
            hospital = Hospital.objects.get(id=form.hospital)
            if not form.middle_name:
                form.middle_name = None
            if not form.birthday:
                form.birthday = '0001-01-01'
                get_data_from_soap = get_client(hospital.api).service.CheckUser(int(form.inn), form.last_name,
                                                                                 form.first_name,
                                                                                 form.middle_name, form.birthday)
            else:
                date = datetime.datetime.strptime(form.birthday, '%d.%m.%Y')
                birthday = date.strftime('%Y-%m-%d')
                get_data_from_soap = get_client(hospital.api).service.CheckUser(int(form.inn), form.last_name,
                                                                                 form.first_name,
                                                                                 form.middle_name, birthday)
            info = serialize_object(get_data_from_soap)
            if info['Assigned'] is True:
                user = User()
                user.username = form.username
                user.email = form.email
                user.password = make_password(form.password2)
                user.first_name = info['FirstName']
                user.last_name = info['LastName']
                user.save()
                user.refresh_from_db()
                user.profile.inn = form.inn
                user.profile.card_id = info['CardId']
                user.profile.middle_name = info['MiddleName']
                user.profile.birthday = info['Birthday']
                print(info['Birthday'])
                user.profile.assigned = info['Assigned']
                user.profile.sex = info['Sex']
                user.profile.department_id = Department.objects.get(department_id=info['DepartmentId'])
                user.profile.hospital_id = form.hospital
                user.profile.save()

                return render(request, 'registration/activation_complete.html')
            else:
                return render(request, 'registration/activation_uncompleted.html')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'registration/registration_form.html', context)


@login_required
def profile_info(request):
    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
    }

    context.update(general_params(request))
    return render(request, 'app/profile.html', context)


@csrf_exempt
def make_appointment(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated():
            time = Schedules.objects.get(id=id)
            user = request.user
            profile = user.profile.card_id

            date = str(time.date.dates) + ' ' + str(time.time)
            dates = dateutil.parser.parse(date)

            doctor_id = request.POST.get('doctor_id')

            doctor = Doctor.objects.get(id=doctor_id)
            med = MedicalService.objects.filter(specification__doctor=doctor).first()

            api = doctor.department.hospital.api

            get_data_from_soap = get_client(api).service.NewOrder(int(profile), med.med_id,
                                                                                            doctor.doc_id, dates)
            info = serialize_object(get_data_from_soap)

            if info != 'Error':
                Appointment.objects.create(appointment_id=info, profile=user.profile, schedule=time)
                time.busy = True
                time.save()

                template = loader.get_template('app/ticket_print.html')
                context = {
                    'name': request.user.get_full_name(),
                    's_date': time.date.dates,
                    'time': time.time,
                    'doctor_name': doctor.get_full_name()
                }
                thread = threading.Thread(target=send_email_notification, args=(
                    'Вы записались к доктору!',
                    template.render(context, request),
                    [user.email]
                ))
                thread.start()

            return JsonResponse(dict(
                success=True, info=info
            ))
        else:
            return JsonResponse(dict(
                success=False, message='Вы должны быть авторизованы!'
            ))
    else:
        return JsonResponse(dict(
            success=False, message='Неверный метод запроса'
        ))


def get_med_records(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    data = get_client(profile.hospital.api).service.GetMedrecords(profile.card_id)
    html = [d['record'] for d in data] if data else '<h1>Результаты не найдены!</h1>'

    context = {
        'user': user,
        'profile': profile,
        'data': data,
        'html': html,
    }

    return render(request, 'app/data.html', context)


# @csrf_exempt
# def make_appointment(request, id):
#     if request.method == 'POST':
#         if request.user.is_authenticated():
#             time = Schedules.objects.get(id=id)
#             user = request.user
#             profile = user.profile.card_id
#
#             date = str(time.date.dates) + ' ' + str(time.time)
#             dates = dateutil.parser.parse(date)
#
#             doctor_id = request.POST.get('doctor_id')
#
#             doctor = Doctor.objects.get(id=doctor_id)
#             med = MedicalService.objects.filter(specification__doctor=doctor).first()
#
#             get_data_from_soap = client.service.NewOrder(int(profile), med.med_id, doctor.doc_id, dates)
#             info = serialize_object(get_data_from_soap)
#
#             if info != 'Error':
#                 Appointment.objects.create(appointment_id=info, profile=user.profile, schedule=time)
#
#             return JsonResponse(dict(
#                 success=True, info=info
#             ))
#         else:
#             return JsonResponse(dict(
#                 success=False, message='Вы должны быть авторизованы!'
#             ))
#     else:
#         return JsonResponse(dict(
#             success=False, message='Неверный метод запроса'
#         ))


@csrf_exempt
def delete_appointment(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated():
            appointment = Appointment.objects.get(id=id)
            appointment_id = appointment.appointment_id

            get_data_from_soap = get_client(appointment.profile.hospital.api).service.DeleteOrder(str(appointment_id))
            info = serialize_object(get_data_from_soap)

            if str(info) == 'True':
                schedule = appointment.schedule
                schedule.busy = False
                schedule.save()

                appointment.delete()

            return JsonResponse(dict(
                success=True, info=info
            ))
        else:
            return JsonResponse(dict(
                success=False, message='Вы должны быть авторизованы!'
            ))
    else:
        return JsonResponse(dict(
            success=False, message='Неверный метод запроса'
        ))


def add_review(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            print(request.POST)
            review = Reviews()
            review.name = user.first_name
            review.text = request.POST.get('text')
            review.doctor_id = request.POST.get('pk')
            review.save()

            template = loader.get_template('partials/review_template.html')
            context = dict(
                comment=review.text,
                name=review.name,
                created_at=review.created_at
            )

            return JsonResponse(dict(success=True, message=template.render(context, request)))

        return JsonResponse(dict(success=False, message='Ваш отзыв не добавлен!'))

    return JsonResponse(dict(success=False, message='Авторизуйтесь, чтобы добавить отзыв'))


def get_ticket(request, appointment_id):
    appointment = Appointment.objects.get(appointment_id=appointment_id, profile__user=request.user)
    params = {
        'name': appointment.profile.user.get_full_name(),
        's_date': appointment.schedule.date,
        'time': appointment.schedule.time,
        'doctor_name': appointment.schedule.doc_id.get_full_name()
    }
    return render(request, 'app/ticket_print.html', params)

def delete_schedules(request):
    schedules = Schedules.objects.all().delete()
    return render(request, 'app/deleted_schedules.html')