from scripts.helpers import *

FIXTURES_PROJECT_FOLDER = os.path.join(base_dir, 'SocialHouse', 'fixtures')
FIXTURE_FOR_ALL_PROJECT_PATH = os.path.join(FIXTURES_PROJECT_FOLDER, 'all_data.json')
FIXTURE_PROVIDING_TEST_PATH = os.path.join(
    APPLICATIONS_FOLDER_PATH, 'social_work', 'providing', 'fixtures', 'providing', 'tests', 'providing.json'
)
FIXTURE_ACTS_TEST_PATH = os.path.join(
    APPLICATIONS_FOLDER_PATH, 'social_work', 'acts', 'fixtures', 'acts', 'tests', 'acts.json'
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
    #     IncludedService(IPPSU=contracts, service=service_10_g_2_day),
    #     IncludedService(IPPSU=contracts, service=service_50_g_2_week),
    #     IncludedService(IPPSU=contracts, service=service_100_g_3_month),
    # ]
    # list(map(lambda incl: incl.save(), included_services))

    journal = ProvidedJournal(
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
    make_fixture(['services', 'people', 'general_info', 'limitations', 'providing', 'contracts', 'auth.user'],
                 FIXTURE_PROVIDING_TEST_PATH, exclude_auth=False)


def acts_tests_fixture():
    d1, d2 = datetime(2020, 1, 1), datetime(2020, 2, 28)
    serviced = generate_serviced(1)[0]
    wp = generate_worker_position()
    ippsu = generate_IPPSU(serviced, wp, d1 - timedelta(days=180))

    journals = create_and_fill_provided_services(ippsu, d1, d2, g_count=30, a_count=15, p_count=30)
    for journal in journals:
        generate_social_act(journal)
        # TODO generate paid act

    print("Make fixture for providing-tests")
    make_fixture(
        ['auth.user', 'people', 'general_info', 'limitations', 'services', 'contracts', 'providing', 'standardization',
         'acts', ],
        FIXTURE_ACTS_TEST_PATH, exclude_auth=False)


def run_all_test_fixtures():
    providing_tests_fixture()
    load_services()
    acts_tests_fixture()


def save_all_data():
    make_fixture(exclude_auth=False, exclude_contenttypes=True)


def reset_all_data():
    tmp = os.path.abspath(os.curdir)
    os.chdir(os.path.dirname(FIXTURE_FOR_ALL_PROJECT_PATH))
    print(os.path.abspath(os.curdir))
    management.call_command(*('loaddata', os.path.basename(FIXTURE_FOR_ALL_PROJECT_PATH)))
    os.chdir(tmp)


if __name__ == '__main__':
    create_superuser()
    # flush_db(create_admin=False)
    # run_all_test_fixtures()
    # save_all_data()

    # run_all_test_fixtures()
    # reset_all_data()
