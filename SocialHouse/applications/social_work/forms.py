from django import forms

# from applications.core.utils import CrispyFormWithSubmit
from applications.social_work.submodels.ippsu import ProvidedService


class ServiceJournalForm(forms.ModelForm):
    class Meta:
        model = ProvidedService
        fields = ['date_of',
                  'service',
                  'ippsu',
                  'type_of_service'  # TODO delete after add signals for checking
                  ]
        widgets = {
            'date_of': forms.DateInput(attrs={'type': 'date'}),
        }
