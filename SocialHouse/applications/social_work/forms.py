from django import forms

# from applications.core.utils import CrispyFormWithSubmit
from applications.core.enums import ServiceTypeEnum
from applications.social_work.models.ippsu import ProvidedService, IncludedService
from applications.social_work.models.services import Service


class ServiceJournalForm(forms.ModelForm):
    class Meta:
        model = ProvidedService
        fields = ['date_of',
                  'service',
                  'journal',
                  # 'type_of_service'  # TODO delete after add signals for checking
                  ]
        widgets = {
            'date_of': forms.DateInput(attrs={'type': 'date'}),
        }


class IncludedServiceForm(forms.ModelForm):
    class Meta:
        model = IncludedService
        fields = ('IPPSU', 'service')

    def __init__(self, *args, **kwargs):
        super(IncludedServiceForm, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(type_of_service=ServiceTypeEnum.GUARANTEED)