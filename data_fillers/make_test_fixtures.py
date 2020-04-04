from applications.social_work.services.models import ServiceMeasurement
from data_fillers.helpers import *

FIXTURES_PROJECT_FOLDER = os.path.join(base_dir, 'SocialHouse', 'fixtures')
FIXTURE_FOR_ALL_PROJECT_PATH = os.path.join(FIXTURES_PROJECT_FOLDER, 'all_data.json')
FIXTURE_PROVIDING_TEST_PATH = os.path.join(
    APPLICATIONS_FOLDER_PATH, 'social_work', 'providing', 'fixtures', 'providing', 'tests', 'providing.json'
)


def make_fixture(apps=None, path_to_fixture=FIXTURE_FOR_ALL_PROJECT_PATH, exclude_auth=True, exclude_contenttypes=True):
    import sys

    args = ['dumpdata', ]
    if apps:
        args += apps
    if exclude_auth:
        args += ['--exclude=auth', ]
    if exclude_contenttypes:
        args += ['--exclude=contenttypes', ]
    args += ['--format=json', '--indent=4']

    # temporary change stdout ot given file
    sysout = sys.stdout
    sys.stdout = open(path_to_fixture, 'w')

    # write json
    management.call_command(*args)

    # change stdout back
    sys.stdout = sysout

    return path_to_fixture


def providing_tests_fixture():
    generate_privileges()
    defaults_for_service = {
        'title': "Тестовая услуга"
    }

    # data for Service
    # Services list and services
    services_list = ServicesList(
        date_from=datetime(2020, 1, 1), date_to=datetime(2025, 1, 1),
    )
    services_list.save()
    defaults_for_service['services_list'] = services_list
    measurement = ServiceMeasurement(
        title="единиц"
    )
    measurement.save()
    defaults_for_service['measurement'] = measurement

    # Limitations
    period_1_day = PeriodLimitation(
        period=PeriodEnum.DAY,
        limit=1
    )
    period_2_week = PeriodLimitation(
        period=PeriodEnum.WEEK,
        limit=2
    )
    period_3_month = PeriodLimitation(
        period=PeriodEnum.MONTH,
        limit=3
    )

    period_1_day.save()
    period_2_week.save()
    period_3_month.save()

    # Day
    volume_10 = VolumeLimitation.objects.get_or_create(limit=10)[0]
    # Week
    volume_50 = VolumeLimitation.objects.get_or_create(limit=50)[0]
    # Month
    volume_100 = VolumeLimitation.objects.get_or_create(limit=100)[0]

    volume_10.save()
    volume_50.save()
    volume_100.save()

    defaults_for_service['type_of_service'] = ServiceTypeEnum.GUARANTEED

    # Services creating
    service_10_g_2_day = Service(
        tax=10,
        volume_limitation=volume_10,
        period_limitation=period_1_day,
        **defaults_for_service,
    )
    service_50_g_2_week = Service(
        tax=50,
        volume_limitation=volume_50,
        period_limitation=period_2_week,
        **defaults_for_service,
    )
    service_100_g_3_month = Service(
        tax=100,
        volume_limitation=volume_100,
        period_limitation=period_3_month,
        **defaults_for_service,
    )

    service_10_g_2_day.save()
    service_50_g_2_week.save()
    service_100_g_3_month.save()

    # data for ProvidedServicesJournal
    wp = generate_worker_position()  # With random FIO
    serviced = generate_serviced(N=1)[0]  # With random FIO
    ippsu = IPPSU(serviced_person=serviced, social_worker=wp,
                  date_from=datetime(2020, 1, 1), date_to=datetime(2023, 1, 1), )
    ippsu.save()
    ippsu.included_services.add(service_10_g_2_day)
    ippsu.included_services.add(service_50_g_2_week)
    ippsu.included_services.add(service_100_g_3_month)
    ippsu.save()
    # included_services = [
    #     IncludedService(IPPSU=ippsu, service=service_10_g_2_day),
    #     IncludedService(IPPSU=ippsu, service=service_50_g_2_week),
    #     IncludedService(IPPSU=ippsu, service=service_100_g_3_month),
    # ]
    # list(map(lambda incl: incl.save(), included_services))

    journal = ProvidedServiceJournal(
        ippsu=ippsu
    )
    journal.save()

    # Making additional and paid services
    defaults_for_service['type_of_service'] = ServiceTypeEnum.ADDITIONAL
    service_100_a = Service(
        volume_limitation=volume_100,
        tax=100,
        **defaults_for_service,
    )
    defaults_for_service['type_of_service'] = ServiceTypeEnum.PAID
    service_10_p = Service(
        volume_limitation=volume_10,
        tax=10,
        **defaults_for_service,
    )
    service_100_a.save()
    service_10_p.save()

    print("Make fixture for providing-tests")
    make_fixture(['services', 'people', 'serviced_data', 'limitations', 'providing', 'ippsu', 'auth.user'],
                 FIXTURE_PROVIDING_TEST_PATH, exclude_auth=False)


if __name__ == '__main__':
    flush_db()
    providing_tests_fixture()
