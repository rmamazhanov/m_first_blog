# coding:utf-8

import django

from base_data_app.models import ParserAPI

django.setup()
from django.conf import settings
from django.core.management.base import BaseCommand
from medical_app.models import Doctor, MedicalService, Specification, Schedules, Date, Hospital, Department
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from zeep.transports import Transport


# with client.options(raw_response=True):
#     responce = service2.Sync()
#
# file = responce.contentt
#
# ns = {"d4p1": "http://rg.kg/mis/webportal.xsd"}
#
# dom = ET.fromstring(file)
#
# doctors = dom.find('.//d4p1:Doctors', ns)
# med_services = dom.find('.//d4p1:Medservices', ns)
# spec = dom.find('.//d4p1:Specs', ns)
# schedules = dom.find('.//d4p1:Schedules', ns)
# hospital = dom.findall('d4p1:Hospital', ns)


class Command(BaseCommand):
    def get_handle(self, file, api_id):
        hospital_id = file['Hospital']['Id']
        hospital_name = file['Hospital']['Name']

        hospital, created = Hospital.objects.get_or_create(hospital_id=hospital_id, name=hospital_name)

        hospital.api_id = api_id
        hospital.save()

        for items in file['Hospital']['Department']:
            dep_id = items['Id']
            dep_name = items['Name']

            departments, created = Department.objects.get_or_create(
                department_id=dep_id, name=dep_name, hospital=hospital)

        for item in file['Doctors']['Doctor']:
            doc_id = item['Id']
            name = item['Name']
            first_name = item['FirstName']
            last_name = item['LastName']
            middle_name = item['MiddleName']
            position = item['Position']
            department_id = item['DepartmentId']

            if not Doctor.objects.filter(doc_id=doc_id).exists():
                doctor, created = Doctor.objects.get_or_create(doc_id=doc_id, name=name, fist_name=first_name,
                                                               last_name=last_name, middle_name=middle_name,
                                                               position=position, department=Department.objects.get(
                        department_id=department_id))

        for services in file['Medservices']['Medservice']:
            med_id = services['Id']
            name = services['Name']
            price = services['Price']

            services, created = MedicalService.objects.get_or_create(med_id=med_id, name=name, price=price)

        for s in file['Specs']['Spec']:
            med_id = s['MedserviceId']
            doc_id = s['DoctorId']
            cab_id = s['CabinetId']

            s, created = Specification.objects.get_or_create(medical_service=MedicalService.objects.get(med_id=med_id),
                                                             doctor=Doctor.objects.get(doc_id=doc_id), cabinet=cab_id)

        for schedule in file['Schedules']['Schedule']:
            date = schedule['Date']

            dates, created = Date.objects.get_or_create(dates=date)

        for schedule in file['Schedules']['Schedule']:
            cab_id = schedule['CabinetId']
            doc_id = schedule['DoctorId']
            date = schedule['Date']
            time = schedule['Time']
            busy = schedule['Busy']

            if busy is False:
                busy = False
                print('False')
            else:
                busy = True
                print('True')

            sche, created = Schedules.objects.get_or_create(cab_id=cab_id,
                                                            doc_id=Doctor.objects.get(doc_id=doc_id),
                                                            date=Date.objects.get(dates=date), time=time,
                                                            busy=busy)

    def handle(self, *args, **options):
        history = HistoryPlugin()
        session = Session()
        session.auth = HTTPBasicAuth('MedML', '12345')

        apis = ParserAPI.objects.filter(is_active=True)

        for api in apis:
            client = Client(api.link,
                            transport=Transport(session=session))

            service2 = client.bind('WebPortal', 'WebPortalSoap12')

            file = client.service.Sync()
            self.get_handle(file, api.id)
