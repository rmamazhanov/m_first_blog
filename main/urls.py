"""medical URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings

from base_data_app.views import index, specialist, medical_services, doctor_reviews, \
    doctor_schedule, signup, profile_info, make_appointment, delete_appointment, get_med_records, \
    news_inner, news, ads, ads_inner, add_review, doctor_detail, doctor_service, get_ticket, delete_schedules

from users.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', auth_views.login, {'template_name': 'app/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name': 'app/logout.html'},  name='logout'),
    url(r'^profile/$', profile_info,  name='profile'),
    url(r'^profile/data/$', get_med_records,  name='get_med_records'),
    url(r'^doctors/$', specialist, name='doctors'),
    url(r'^doctors/(?P<pk>[0-9]+)$', doctor_detail, name='doctor_detail'),
    url(r'^doctors/(?P<pk>[0-9]+)/schedule/$', doctor_schedule, name='doctor_schedule'),
    url(r'^doctors/(?P<pk>[0-9]+)/reviews/$', doctor_reviews, name='doctor_reviews'),
    url(r'^doctors/(?P<pk>[0-9]+)/services/$', doctor_service, name='doctor_services'),
    url(r'^make_appointment/(?P<id>[0-9]+)/', make_appointment, name='make_appointment'),
    url(r'^delete_appointment/(?P<id>[0-9]+)/', delete_appointment, name='delete_appointment'),
    url(r'^services/$', medical_services, name='services'),
    url(r'^delete-schedules/$', delete_schedules, name='delete_schedules'),
    url(r'^news/$', news, name='news'),
    url(r'^news/(?P<id>[0-9]+)$', news_inner, name='news_inner'),
    url(r'^ads/$', ads, name='ads'),
    url(r'^ads/(?P<id>[0-9]+)$', ads_inner, name='ads_inner'),
    url(r'^add_review$', add_review, name='add_review'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^password/recovery/request/$', request_password_recovery, name='request_password_recovery'),
    url(r'^password/recovery/change/(?P<session_hash>[0-9A-Za-z_\-]+)$', show_set_password_form, name='show_set_password_form'),
    url(r'^ticket/(?P<appointment_id>[\w-]+)/$', get_ticket, name='get_ticket')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

