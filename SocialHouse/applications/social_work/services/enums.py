from django.db.models.enums import TextChoices


class ServiceTypeEnum(TextChoices):
    GUARANTEED = 'G', "гарантированная"
    ADDITIONAL = 'A', "дополнительная"
    PAID = 'P', "платная"
    PAID_FROM_GUARANTEED = 'F', "платная (гарантия)"
    CALCULATING = 'C', "-вычисляется-"

    def __eq__(self, other):
        # If self P and other is PfG
        if self.value == self.PAID.value or self.value == self.PAID_FROM_GUARANTEED.value:
            if other == self.PAID_FROM_GUARANTEED.value or other == self.PAID.value:
                return True
        # self.value
        # if self.PAID_FROM_GUARANTEED.value and other or self.PAID.value and other:
        #     return True
        return super().__eq__(other)


class ServiceCategoryEnum(TextChoices):
    WELFARE = 'SB', "Социально-бытовые услуги"
    MEDICINE = 'ME', "Социально-медицинские услуги"
    PSYCHOLOGY = 'PS', "Социально-психологические услуги"
    PEDAGOGICAL = 'ED', "Социально-педагогические услуги"
    LABOUR = 'WO', "Социально-трудовые услуги"
    LAW = 'LA', "Социально-правовые услуги"
    COMMUNICATE = 'CO', "Услуги в целях повышения коммуникативного потенциала получателей социальных услуг " \
                        "имеющих ограничения жизнедеятельности, в том числе детей-инвалидов"
    RELIEF = 'QU', "Срочные социальные услуги"
    OTHER = 'OT', "-Прочие"
    __empty__ = "Не указано"
