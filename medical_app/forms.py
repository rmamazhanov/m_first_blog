from django.forms import *


class MedicalServiceForm(Form):

    name = ChoiceField()


class DepartmentForm(Form):

    name = ChoiceField()