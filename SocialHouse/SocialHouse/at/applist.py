all_models = {

    "Обслуживаемые": (
        'applications.department.people.models.people.ServicedPerson',
        'applications.department.general_info.models.data.PassportData',
        'applications.department.general_info.models.data.Privilege',
    ),
    "Работники": (
        'applications.department.people.models.people.Worker',
        'applications.department.people.models.people.WorkerPosition',
    ),
    "Оказание услуг": (
        'applications.department.people.models.people.ServicedPerson',
        'applications.documentation.contracts.models.IPPSU',
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
        'applications.receptionist.night_shifts.models.NightShift',
        'applications.receptionist.night_shifts.models.ServicedPersonOvernight',
        'applications.receptionist.night_shifts.models.VisitorOvernight',
        'applications.receptionist.movements.models.SickLeave',
        'applications.receptionist.movements.models.Travel',
    )
}

persons_models = {
    "Обслуживаемые": (
        'applications.department.people.models.people.ServicedPerson',
        'applications.department.people_data.models.serviced_data.PassportData',
        'applications.department.people_data.models.serviced_data.PrivilegeCertificate',
        'applications.department.income_data.models.AveragePerCapitaIncome',
    ),
    "Договоры": (
        'applications.documentation.contracts.models.contracts.SocialContract',
        'applications.documentation.contracts.models.contracts.PaidContract',
        'applications.documentation.contracts.models.ippsu.IPPSU',
    ),
    "Работники": {
        'applications.department.people.models.people.Worker',
        'applications.department.people.models.people.WorkerPosition',
    }
}

department = {

    "Внешние данные": (
        'applications.department.people_data.models.serviced_data.Privilege',
        'applications.department.income_data.models.LivingWage',
    ),

    "События": (
        'applications.department.events.models.Event',
    ),
    "Информация об отделении": (
        'applications.department.general_data.models.DepartmentInfo',
    ),
}

social_work = {
    "Оказание услуг": (
        'applications.social_work.providing.models.ProvidedJournal',
        'applications.social_work.providing.models.ProvidedService',

        'applications.documentation.acts.models.paid.PaidAct',
        'applications.documentation.acts.models.social.SocialAct',
    ),
    "Перечни услуг": (
        'applications.social_work.services.models.ServicesList',
        'applications.social_work.services.models.Service',
        'applications.social_work.services.models.ServiceMeasurement',

        'applications.social_work.limitations.models.VolumeLimitation',
        'applications.social_work.limitations.models.PeriodLimitation',
    ),
}

documentation = {
    "Месяц": (
        'applications.documentation.acts.models.paid.PaidAct',
        'applications.documentation.acts.models.social.SocialAct',

        'applications.documentation.reports.models.month.RegistryMonthly',
        'applications.documentation.reports.models.month.DigitalMonthlyReport',
    ),
    "Квартал": (
        'applications.documentation.reports.models.quarter.QuarterAct',
        'applications.documentation.reports.models.quarter.QuarterReportPrivileges',
    ),
    "Год": (
        'applications.documentation.reports.models.year.DigitalYearReport',
        'applications.documentation.reports.models.year.CommonYearReport',
        'applications.documentation.reports.models.year.MeterDataInfo',
    ),
    "Договоры": (
        'applications.documentation.contracts.models.contracts.SocialContract',
        'applications.documentation.contracts.models.contracts.PaidContract',
        'applications.documentation.contracts.models.ippsu.IPPSU',
    ),

    "Заявления": (
        'applications.documentation.letters.models.contracts.LetterContract',
        'applications.documentation.letters.models.visitor.LetterVisitor',
    ),

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
        'applications.receptionist.night_shifts.models.NightShift',
        'applications.receptionist.night_shifts.models.ServicedPersonOvernight',
        'applications.receptionist.night_shifts.models.VisitorOvernight',
        'applications.receptionist.movements.models.SickLeave',
        'applications.receptionist.movements.models.Travel',
    )
}
