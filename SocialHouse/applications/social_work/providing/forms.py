from django import forms

from applications.social_work.providing.models import ProvidedService


class ProvidedServiceForm(forms.ModelForm):
    class Meta:
        model = ProvidedService
        fields = [
            # 'date_from',
            'service',
            'journal',
            # 'type_of_service'  # TODO delete after add signals for checking
        ]
        widgets = {
            'date_from': forms.DateInput(attrs={'type': 'date'}),
        }
