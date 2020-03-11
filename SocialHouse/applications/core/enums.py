from choicesenum import ChoicesEnum


class ServiceTypeEnum(ChoicesEnum):
    GUARANTEED = 'G', "гарантированная"
    ADDITIONAL = 'A', "дополнительная"
    PAID = 'P', "платная"
    CALCULATING = 'C', "-вычисляется-"
    UNDEFINED = 'U', "-неопределенно-"


class WorkerPositionEnum(ChoicesEnum):
    CHIEF = 'C', "Заведующий отделением"
    SOCIAL_WORKER = 'S', "Социальный работник"
    NURSE = 'N', "Сиделка"
    RECEPTIONIST = 'R', "Администратор отделения"
