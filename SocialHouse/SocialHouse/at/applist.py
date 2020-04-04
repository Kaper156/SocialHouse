all_models = {
    "Обслуживаемые": (
        'applications.people.models.people.ServicedPerson',
        'applications.serviced_data.models.data.PassportData',
        'applications.serviced_data.models.data.Privilege',
    ),
    "Работники": (
        'applications.people.models.people.Worker',
        'applications.people.models.people.WorkerPosition',
    ),
    "Оказание услуг": (
        'applications.people.models.people.ServicedPerson',
        'applications.social_work.ippsu.models.IPPSU',
        'applications.social_work.providing.models.ProvidedService',
    ),
    "Хранимые услуги": (
        'applications.social_work.services.models.ServiceMeasurement',
        'applications.social_work.services.models.ServicesList',
        'applications.social_work.services.models.Service',
        'applications.social_work.limitations.models.VolumeLimitation',
        'applications.social_work.limitations.models.PeriodLimitation',

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
