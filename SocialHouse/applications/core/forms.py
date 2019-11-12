from django import forms

from applications.core.utils import CrispyFormWithSubmit
from .models import ServicedPerson, PassportData


class ServicedPersonForm(CrispyFormWithSubmit, forms.ModelForm):
    __submit_text__ = 'Добавить нового осблуживаемого'

    class Meta:
        model = ServicedPerson
        fields = ['name',
                  'patronymic',
                  'surname',
                  'gender',
                  'date_of_birth',
                  'location',
                  ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class PassportDataForm(CrispyFormWithSubmit, forms.ModelForm):
    __submit_text__ = 'Добавить пасспортные данные'

    class Meta:
        model = PassportData
        fields = ['serial',
                  'number',
                  'date_of_issue',
                  'serviced_person',
                  ]
        widgets = {
            'date_of_issue': forms.DateInput(attrs={'type': 'date'}),
        }
