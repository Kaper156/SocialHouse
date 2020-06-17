from django.db.models.signals import pre_save

from .models import IPPSU, SocialContract, PaidContract
from ..standardization.signals import document_pre_save

pre_save.connect(document_pre_save, sender=IPPSU)
pre_save.connect(document_pre_save, sender=SocialContract)
pre_save.connect(document_pre_save, sender=PaidContract)
