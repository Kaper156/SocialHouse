from django import forms

from applications.core.utils import CrispyFormWithSubmit
from .models import ServiceJournal


class ServiceJournalForm(CrispyFormWithSubmit, forms.ModelForm):
    __submit_text__ = 'Сохранить оказанную услугу'

    class Meta:
        model = ServiceJournal
        fields = ['date_of',
                  'serviced',
                  'employer',
                  'service',
                  'type_of_service'  # TODO delete after add signals for checking
                  ]
        widgets = {
            'date_of': forms.DateInput(attrs={'type': 'date'}),
        }
