from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from zeep.transports import Transport

from base_data_app.models import ParserAPI
from main import settings
from medical_app.models import Hospital


def get_client(api):
    history = HistoryPlugin()
    session = Session()
    session.auth = HTTPBasicAuth('MedML', '12345')
    try:
        parserApi = ParserAPI.objects.get(id=api.id)
    except:
        parserApi = None
    client = Client(parserApi.link if parserApi else settings.PARSER_API,
                    transport=Transport(session=session))
    return client


def client_check_user(inn, last_name=None, first_name=None, middle_name=None, birthday=None):
    parser_apis = ParserAPI.objects.filter(is_active=True)

    for api in parser_apis:
        session = Session()
        session.auth = HTTPBasicAuth('MedML', '12345')
        client = Client(api.link, transport=Transport(session=session))
        client.service.CheckUser()

