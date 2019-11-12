from django import forms

from applications.core.utils import CrispyFormWithSubmit
from .models import ServicedPerson


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
