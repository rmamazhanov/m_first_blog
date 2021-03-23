# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import threading

from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import User

# Create your views here.



def send_email_notification(title, body, to):
    email = EmailMessage(title, body=body, to=to)
    email.content_subtype = 'html'
    email.send()


def request_password_recovery(request):
    params = {

    }
    if request.POST:
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)

            protocol = 'https://' if request.is_secure() else 'http://'
            url = protocol + request.get_host() + reverse(
                'show_set_password_form',
                kwargs={
                    'session_hash': urlsafe_base64_encode(email.encode('ascii'))
                }
            )
            template = loader.get_template('partials/recovery_reuest.html')
            body = template.render({
                'link': url
            }, request)
            thread = threading.Thread(target=send_email_notification, args=(
                'Восстановление пароля | Медицинский портал электронной очереди',
                body,
                [email]
            ))
            thread.start()
            params['email'] = email
            params['message'] = 'Мы отправили вам инструкции по E-Mail, пожалуйста проследуйте им!'
        except ObjectDoesNotExist:
            params['error'] = 'Пользователя с таким E-Mail не существует'

    return render(request, 'app/password_recovery_request.html', params)


def show_set_password_form(request, session_hash):
    check_word = urlsafe_base64_decode(session_hash)
    params = {

    }

    if request.POST:
        email = check_word
        password = request.POST.get('password')
        password1 = request.POST.get('re_password')
        if password == password1:
            try:
                user = User.objects.get(email=email)

                user.password = make_password(password1)
                user.save()
                login(request=request, user=user)
                return HttpResponseRedirect(reverse('profile'))
            except ObjectDoesNotExist:
                params['is_ok'] = False
                params['message'] = 'Пользователь не найден'
        else:
            params['is_ok'] = False
            params['message'] = 'Пароли не совпадают'

    return render(request, 'app/password_recovery_form.html', params)