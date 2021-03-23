import datetime
from django import template

from medical_app.forms import MedicalServiceForm
from medical_app.models import *

from dateutil import parser

register = template.Library()


@register.inclusion_tag('app/specialist.html')
def show_week_day_name(days):
    week_day = days.date.strftime("%a")
    return {'week_day': week_day}


@register.assignment_tag
def get_schedule_by_doctor_id(doctor_id, day):
    return Schedules.objects.filter(doc_id=doctor_id, date=day)


@register.assignment_tag
def get_medical_service_form_for_instance(doctor_instance):
    medical_services = MedicalService.objects.filter(specification__doctor=doctor_instance)
    form = MedicalServiceForm()

    form.fields['name'].choices = ((medical_service.pk, medical_service.name) for medical_service in medical_services)

    return form


@register.assignment_tag
def is_earlier_than_today(date):
    today = datetime.date.today()

    return (today - date).days > 0


@register.assignment_tag
def is_earlier_than_now(time, date):
    if not isinstance(date, datetime.date):
        d = str(date)
        date = datetime.date(int(d.split('-')[0]), int(d.split('-')[1]), int(d.split('-')[2]))
    return datetime.datetime.now().hour + 2 - time.hour >= 2 and (datetime.date.today() - date).days == 0


@register.assignment_tag
def get_service_by_doctor(doctor):
    return MedicalService.objects.filter(specification__doctor=doctor).first()


@register.assignment_tag
def format_date_time(date, time):
    date = str(date) + ' ' + str(time)
    dates = parser.parse(date)

    return dates.strftime('%d\\%m %H:%M')


@register.assignment_tag
def not_is_now(time):
    t = datetime.time(time.hour, time.minute)
    print((datetime.datetime.now().hour + 1), t.hour)
    return (datetime.datetime.now().hour + 1) <= t.hour


@register.simple_tag
def prepare_url(url, param):
    if '?' in url:
        b = url.split('?')[0]
        url = url.split('?')[1]
        if '&' in url:
            params = url.split('&')

            new_params = []
            for p in params:
                k = p.split('=')[0]
                if k != param:
                    new_params.append(p)

            return b + '?' + '&'.join(new_params) + '&'
        else:
            if '=' in url:
                _k = url.split('=')[0]
                if _k == param:
                    return b + '?'
                return b + '?' + url + '&'
            return b + '?'
    return url + '?'


