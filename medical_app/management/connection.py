# -*- coding: utf-8 -*-
import codecs

import datetime
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from zeep.transports import Transport
from zeep.helpers import serialize_object




# def connect1C():
#     history = HistoryPlugin()
#     session = Session()
#     session.auth = HTTPBasicAuth('MedML', '12345')
#
#     client = Client('http://1c.rg.kg:8888/portal/ws/wsWebPortal.1cws?wsdl',
#                     transport=Transport(session=session))
#
# a = client.service.Sync()
# service2 = client.bind('WebPortal', 'WebPortalSoap12')
#
#     service = client.create_service(
#         '{http://rg.kg/mis/portal}WebPortalSoap12Binding', 'http://rg.kg/mis/portal')
#
# print (a)




history = HistoryPlugin()
session = Session()
session.auth = HTTPBasicAuth('MedML', '12345')

client = Client('http://178.216.210.23/portal/ws/wsWebPortal.1cws?wsdl',
                transport=Transport(session=session))

service2 = client.bind('WebPortal', 'WebPortalSoap12')
#
# a = client.service.Sync()
# d = datetime.datetime.strptime("2013-1-25", '%Y-%m-%d')
# print (datetime.date.strftime(d, "%m-%d-%Y"))
# print(a['Hospital']['Schedules'])
# print(a['Hospital'])
# print(a['Hospital']['Id'])
# print(a['Hospital']['Name'])
# for i in (a['Hospital']['Department']):
#     print(i['Id'], i['Name'])

# for schedule in a['Schedules']['Schedule']:
#     d = datetime.datetime.strptime(str(schedule['Date']), '%Y-%m-%d')
#     print(schedule['CabinetId'], datetime.date.strftime(d, "%m-%d-%Y"))




# print (a)
# b = serialize_object(a)
# print (b)
#
# with client.options(raw_response=True):
#     response = service2.Sync()

# a = response
#
# # print(dir(a.json))
# print(a)
# # print (a)
# # #
# # inn = '10108199900391'
# # with client.options():
# #     responce = service2.CheckUser(int(inn))
# #     a = responce
# #
# # print (a)
# # from zeep.wsdl.utils import etree_to_string
# #
# # def make_soap_request_data(client, operation, *args, **kwargs):
# #     service = client.service
# #     binding = service._binding
# #     envelope, headers = binding._create(operation, args, kwargs, client=client, options=service._binding_options)
# #     xml = etree_to_string(envelope)
# #     print (xml, headers)
# # from zeep.helpers import serialize_object
# # dom = serialize_object(a)
# # ns = {"d4p1": "http://rg.kg/mis/webportal.xsd"}
# # doctors = dom.find('d4p1:Doctors', ns)
# # doctors = dom['Hospital']
# # #
# # print (dom)
# # for department in doctors:
# #     print (department['id'])
#
#
# # print(doctors)
# # for doctor in doctors:
# #     doc_id = doctor.find('.//d4p1:Id', ns).text
# #     name = doctor.find('.//d4p1:Name', ns).text
# #
# #     print(doc_id, name)
#
# # #
#
#
# # b = client.service.Sync()
#
# # print (b)
# # # try:
birthday = '1983-12-31'
last_name = 'Тимофеев'
first_name = 'Максим'
middle_name = 'Анатольевич'
inn = '83006195713010'
c = client.service.CheckUser(int(inn), last_name, first_name, middle_name, birthday)
print(c)
# c = client.service.GetMedrecords(15599)
# d = serialize_object(c)
# print(d.keys())
# # print (d['Assigned'])
# file = open('collection.txt', 'w')
# file.write(str(a))
# file.close()
#
# print(len(c))
# p = [d['record'] for d in c]
#
# for i in p:
#     print(i)

# except Fault as error:
#     foo = error.detail
#     print (foo)








