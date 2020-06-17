from django import forms

from .models.serviced_data import PassportData


class PassportDataForm(forms.ModelForm):
    __submit_text__ = 'Добавить пасспортные данные'

    class Meta:
        model = PassportData
        fields = ['serial',
                  'number',
                  'date_of_issue',
                  # 'serviced_person',
                  ]
        # Todo add serviced_person as readonly
        widgets = {
            'date_of_issue': forms.DateInput(attrs={'type': 'date'}),
        }
