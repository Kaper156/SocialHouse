from django import forms

from .models import ServicedPerson, PassportData


class ServicedPersonForm(forms.ModelForm):
    class Meta:
        model = ServicedPerson
        fields = ['name',
                  'patronymic',
                  'surname',
                  'gender',
                  'date_of_birth',
                  'location',
                  'privileges'
                  ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class PassportDataForm(forms.ModelForm):
    __submit_text__ = 'Добавить пасспортные данные'

    class Meta:
        model = PassportData
        fields = ['serial',
                  'number',
                  'date_of_issue',
                  # 'serviced_person',
                  ]
        widgets = {
            'date_of_issue': forms.DateInput(attrs={'type': 'date'}),
        }
