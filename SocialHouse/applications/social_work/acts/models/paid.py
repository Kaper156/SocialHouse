from applications.social_work.acts.models.abstract import Act


class PaidAct(Act):
    class Meta:
        abstract = False
        verbose_name = "Акты платных услуг"
        verbose_name_plural = "Акт платных услуг"
