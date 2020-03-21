from django import forms

from applications.people.models.people import ServicedPerson


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
