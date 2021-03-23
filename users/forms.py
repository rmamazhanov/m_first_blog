from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from medical_app.models import Hospital


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    inn = forms.IntegerField(required=False)
    middle_name = forms.CharField(max_length=30, required=False)
    birthday = forms.DateField(required=False)
    hospital = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        hospitals = Hospital.objects.all()
        choices = ((None, '-------'),)
        for h in hospitals:
            choices += (h.id, h.name),
        self.fields['hospital'].widget = forms.Select(choices=choices, attrs={
            'class': 'uk-select'
        })


    class Meta:
        model = User
        fields = ('inn', 'username', 'first_name', 'last_name', 'middle_name', 'birthday')
