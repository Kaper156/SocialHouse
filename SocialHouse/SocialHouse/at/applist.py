all_models = {
    "Обслуживаемые": (
        'applications.core.models.ServicedPerson',
        'applications.core.models.PassportData',
        'applications.core.models.Privilege',
    ),
    "Работники": (
        'applications.core.models.Worker',
        'applications.core.models.Position',
        'applications.core.models.WorkerPosition',
    ),
    "Оказание услуг": (
        'applications.core.models.ServicedPerson',
        'applications.social_work.submodels.ippsu.IPPSU',
        'applications.social_work.submodels.ippsu.IncludedService',
        'applications.social_work.submodels.ippsu.ProvidedService',
    ),
    "Хранимые услуги": (
        'applications.social_work.submodels.services.ServiceMeasurement',
        'applications.social_work.submodels.services.ServicesList',
        'applications.social_work.submodels.services.Service',
    ),
    "Учет проживающих": (
        'applications.receptionist.visits.models.Visit',
        'applications.receptionist.visits.models.Visitor',
        'applications.receptionist.overnight.models.NightShift',
        'applications.receptionist.overnight.models.ServicedPersonOvernight',
        'applications.receptionist.overnight.models.VisitorOvernight',
        'applications.leaving.models.SickLeave',
        'applications.leaving.models.Travel',
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
        'applications.receptionist.overnight.models.NightShift',
        'applications.receptionist.overnight.models.ServicedPersonOvernight',
        'applications.receptionist.overnight.models.VisitorOvernight',
        'applications.leaving.models.SickLeave',
        'applications.leaving.models.Travel',
    )
}
