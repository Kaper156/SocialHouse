from django import forms

from applications.core.models import ServicedPerson
from applications.core.utils import CrispyFormWithSubmit


class ServicedPersonForm(CrispyFormWithSubmit, forms.ModelForm):
    __submit_text__ = 'Добавить нового осблуживаемого'

    class Meta:
        model = ServicedPerson
        fields = ['name',
                  'patronymic',
                  'surname',
                  'gender',
                  'date_of_birth',
                  'status',
                  ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'datepicker'}),
        }
