all_models = {
    "Обслуживаемые": (
        'applications.core.models.people.ServicedPerson',
        'applications.core.models.serviced_data.PassportData',
        'applications.core.models.serviced_data.Privilege',
    ),
    "Работники": (
        'applications.core.models.people.Worker',
        'applications.core.models.people.WorkerPosition',
    ),
    "Оказание услуг": (
        'applications.core.models.ServicedPerson',
        'applications.social_work.models.ippsu.IPPSU',
        'applications.social_work.models.ippsu.IncludedService',
        'applications.social_work.models.ippsu.ProvidedService',
    ),
    "Хранимые услуги": (
        'applications.social_work.models.services.ServiceMeasurement',
        'applications.social_work.models.services.ServicesList',
        'applications.social_work.models.services.Service',
    ),
    "Учет проживающих": (
        'applications.receptionist.visits.models.Visit',
        'applications.receptionist.visits.models.Visitor',
        'applications.receptionist.sleepover.models.NightShift',
        'applications.receptionist.sleepover.models.ServicedPersonOvernight',
        'applications.receptionist.sleepover.models.VisitorOvernight',
        'applications.receptionist.movements.models.SickLeave',
        'applications.receptionist.movements.models.Travel',
    )
}

receptionist_models = {
    "Коммунальные услуги": (
        'applications.receptionist.meter.models.Meter',
        'applications.receptionist.meter.models.MeterData',
        'applications.receptionist.meter.models.SealingMeter',
        'applications.receptionist.meter.models.UtilityBil',
    ),
    "Учет проживающих": (
        'applications.receptionist.visits.models.Visit',
        'applications.receptionist.visits.models.Visitor',
        'applications.receptionist.sleepover.models.NightShift',
        'applications.receptionist.sleepover.models.ServicedPersonOvernight',
        'applications.receptionist.sleepover.models.VisitorOvernight',
        'applications.receptionist.movements.models.SickLeave',
        'applications.receptionist.movements.models.Travel',
    )
}
