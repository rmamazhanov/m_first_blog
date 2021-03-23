# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from base_data_app.models import Slider, Contacts, AboutUs, News, CompanyNumbers, Team, Reviews, Partners, FaqCategory, \
    Faq, FreeConsulting, FeedBack, Certificates, Features, Subscribers, Ads, ParserAPI


class SliderAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Slider


class AboutUsAdmin(admin.ModelAdmin):
    model = AboutUs

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return True
        else:
            return False


class ContactsAdmin(admin.ModelAdmin):
    model = Contacts

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return True
        else:
            return False


class FeaturesAdmin(admin.ModelAdmin):
    save_as = True


class ParserAdmin(admin.ModelAdmin):
    list_display = ['id', 'link', 'is_active']
    list_editable = ['link']



# Register your models here.
admin.site.register(Slider, SliderAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(News)
admin.site.register(CompanyNumbers)
admin.site.register(Team)
admin.site.register(Reviews)
admin.site.register(Partners)
admin.site.register(FaqCategory)
admin.site.register(Faq)
admin.site.register(FreeConsulting)
admin.site.register(FeedBack)
admin.site.register(Certificates)
admin.site.register(Features, FeaturesAdmin)
admin.site.register(Subscribers)
admin.site.register(Ads)
admin.site.register(ParserAPI, ParserAdmin)
