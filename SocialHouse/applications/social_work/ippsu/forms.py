from django import forms

from applications.social_work.services.enums import ServiceTypeEnum
from applications.social_work.services.models import Service
from .models import IncludedService


class IncludedServiceForm(forms.ModelForm):
    class Meta:
        model = IncludedService
        fields = ('IPPSU', 'service')

    def __init__(self, *args, **kwargs):
        super(IncludedServiceForm, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(type_of_service=ServiceTypeEnum.GUARANTEED)
