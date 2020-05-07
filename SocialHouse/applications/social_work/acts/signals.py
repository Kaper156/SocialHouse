from django.db.models.signals import pre_save

from applications.documents.signals import document_pre_save
from .models import SocialAct, PaidAct

pre_save.connect(document_pre_save, sender=SocialAct)
pre_save.connect(document_pre_save, sender=PaidAct)
