import os
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialHouse.settings.dev')

import django

from faker import Faker
from random import randint, choice

django.setup()
from applications.core.models import ServicedPerson, Privilege, PassportData, User, Worker, WorkerPosition

from applications.core.enums import WorkerPositionEnum, ServiceTypeEnum
from applications.core.utils.datetime import range_month, random_date_between
from applications.social_work.models import IPPSU, IncludedService, Service, ServicesList, ProvidedServiceJournal, \
    ProvidedService

faker = Faker(locale='ru_RU')
PASSWORD_FOR_TEST_USERS = 'aq12wsde3'


def generate_privileges():
    privs = (
        "Ветераны труда",
        "Труженики тыла",
        "Реабилитированные лица",
        "Лица, пострадавшие от политических репрессий",
        "Ветераны Омской области",
        "Герой СССР, Герой РФ, Герой Соц. труда, полный кавалер ордена Трудовой Славы и члены их семей",
        "Участники боевых действий и члены их семей",
        "Женщины-участницы Великой Отечественной войны",
        "Награжденные медалью 'За оборону Ленинграда', знаком 'Жителю блокадного Ленинграда'",
        "Лица, проживающие на территории Омской области, которым по состоянию на 9 мая 1945 года не исполнилось 18 лет и родители (один из родителей) которых в период с 22 июня 1941 года по 9 мая 1945 года погибли (пропали без вести), умерли в указанный период вследствие ранения, увечья или заболевания, полученных при защите Отечества или исполнении обязанностей военной службы на фронте, в районах боевых действий",
        "Члены семей погибших (умерших) инвалидов войны, участников Великой Отечественной войны и ветеранов боевых действий, члены семей погибших в Великой Отечественной войне лиц из числа личного состава групп самозащиты объектовых и аварийных команд местной противовоздушной обороны, а также члены семей погибших работников госпиталей и больниц города Ленинграда",
        "Пострадавшие от техногенных катастроф",
        "'Почетный донор России', 'Почетный донор СССР'",
        "Граждане, имеющие почетные звания",
        "Инвалиды",
    )

    for p in privs:
        Privilege(title=p).save()


def generate_user(nick):
    user = User.objects.get_or_create(
        username=nick
    )[0]
    user.set_password(PASSWORD_FOR_TEST_USERS)
    user.save()
    return user


def generate_worker(status):
    user = generate_user(faker.simple_profile('M')['username'])

    if randint(1, 10) % 2:
        # Male
        gender = 'M'
        name = faker.first_name_male()
        patronymic = faker.middle_name_male()
        surname = faker.last_name_male()
    else:
        # Female
        gender = 'F'
        name = faker.first_name_female()
        patronymic = faker.middle_name_female()
        surname = faker.last_name_female()
    date_of_birth = faker.date_of_birth(tzinfo=None, minimum_age=25, maximum_age=55)

    worker = Worker.objects.get_or_create(
        user=user,
        gender=gender,
        name=name,
        patronymic=patronymic,
        surname=surname,
        date_of_birth=date_of_birth,
        status=status,
    )[0]
    worker.save()
    return worker


def generate_worker_position(worker=None, position=WorkerPositionEnum.SOCIAL_WORKER, is_dismiss=False):
    worker = worker or generate_worker(Worker.STATUSES[0][0])

    date_of_appointment = faker.date_of_birth(tzinfo=None, minimum_age=1, maximum_age=5)

    worker_position = WorkerPosition.objects.get_or_create(
        worker=worker,
        position=position,
        date_of_appointment=date_of_appointment,
        rate=1
    )[0]

    if is_dismiss:
        worker_position.dismissal_date = datetime.now().date() - timedelta(days=randint(1, 180))
    worker_position.save()
    return worker_position


def get_all_services():
    return ServicesList.objects.last().service_set.all()


def create_included_services(ippsu, cnt=30):
    already_included_services = None
    # Service.objects.filter(pk=a.included_services.values('service_id', flat=True))
    # if Service.objects.filter(pk=ippsu.included_services.values('service', flat=True)).exists():
    # already_included_services = Service.objects.filter(pk=ippsu.included_services.values('service'))
    already_included_services = Service.objects.filter(includedservice__IPPSU=ippsu)
    # already_included_services = ippsu.included_services.values('service', flat=True)
    all_services = get_all_services()
    not_included_services = all_services.exclude(id__in=already_included_services.values('id'))
    while cnt:
        service = choice(not_included_services)
        included_service = IncludedService.objects.get_or_create(
            service=service,
            IPPSU=ippsu
        )[0]
        included_service.save()
        not_included_services = not_included_services.exclude(pk=service.pk)
        cnt -= 1


def generate_IPPSU(serviced_person, social_worker, date_from, date_to=None, cnt_included=30):
    ippsu = IPPSU.objects.get_or_create(
        serviced_person=serviced_person,
        social_worker=social_worker,
        date_from=date_from
    )[0]
    if date_to:
        ippsu.date_to = date_to
    ippsu.save()

    create_included_services(ippsu=ippsu, cnt=cnt_included)
    return ippsu


def create_and_fill_IPPSU_serviced_workers():
    cnt_workers = 3
    # Exclude dead and leaved
    serviced = ServicedPerson.objects.exclude(location='LE').exclude(location='DE')
    serviced_per_worker = serviced.count() // cnt_workers
    for cur_worker_number in range(cnt_workers):
        worker_position = generate_worker_position()
        for cur_serviced_number in range(serviced_per_worker):
            serviced_person = serviced[(cur_worker_number + 1) * cur_serviced_number]

            # Second IPPSU can be added
            # if serviced_person.date_of_income - datetime.now().date() < timedelta(days=365 * 3):
            date_from = min(serviced_person.date_of_income, datetime.now().date() - timedelta(days=365 * 3 - 54))
            ippsu = generate_IPPSU(serviced_person, worker_position, date_from=date_from, cnt_included=randint(25, 34))
            yield ippsu


def pop_random_obj_from_q(queryset):
    random_obj = choice(queryset)
    queryset.exclude(pk=random_obj.id)
    return random_obj, queryset


def generate_provided_service(journal, service, date1, date2):
    date_of = random_date_between(date1, date2)
    volume = randint(1, service.measurement.volume_statement.limit * 2)
    quantity = randint(1, service.measurement.period_statement.limit * 2)

    provided_service = ProvidedService.objects.get_or_create(
        journal=journal,
        date_of=date_of,
        service=service,
        volume=volume,
        quantity=quantity,

    )[0]
    provided_service.save()


def create_and_fill_provided_services(ippsu, date_from=None, date_to=None, g_count=None, a_count=None, p_count=None):
    # for ippsu in IPPSU.objects.filter(is_archived=False):
    # TODO for many months
    # Be careful create only first and last month journal
    date_range = {range_month(date_from), range_month(date_to)}

    for date1, date2 in date_range:
        journal = ProvidedServiceJournal.objects.get_or_create(
            ippsu=ippsu,
            date_from=date1,
            date_to=date2,
        )[0]
        journal.save()

        # TODO Add it as manager
        guaranteed = Service.objects.filter(includedservice__IPPSU=ippsu)
        additional = get_all_services().filter(type_of_service=ServiceTypeEnum.ADDITIONAL)
        paid = get_all_services().filter(type_of_service=ServiceTypeEnum.PAID)

        for g in range(g_count or 20):
            service, guaranteed = pop_random_obj_from_q(guaranteed)
            generate_provided_service(journal, service, date1, date2)
        for a in range(a_count or 15):
            service, additional = pop_random_obj_from_q(additional)
            generate_provided_service(journal, service, date1, date2)
        for p in range(p_count or 5):
            service, paid = pop_random_obj_from_q(paid)
            generate_provided_service(journal, service, date1, date2)


def generate_serviced(N=30, dead=False, left=False, location=None):
    privils = Privilege.objects.all()
    for i in range(N):
        name, patronymic, surname = '', '', ''
        if randint(1, 10) % 2:
            # Male
            gender = 'M'
            name = faker.first_name_male()
            patronymic = faker.middle_name_male()
            surname = faker.last_name_male()
        else:
            # Female
            gender = 'F'
            name = faker.first_name_female()
            patronymic = faker.middle_name_female()
            surname = faker.last_name_female()
        date_of_birth = faker.date_of_birth(tzinfo=None, minimum_age=50, maximum_age=98)

        serviced = ServicedPerson(
            name=name,
            patronymic=patronymic,
            surname=surname,
            gender=gender,
            date_of_birth=date_of_birth
        )
        if dead:
            serviced.date_of_death = faker.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=3)
        if left:
            serviced.date_of_departure = faker.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=3)
        if location:
            serviced.location = location
        serviced.save()
        for _ in range(randint(randint(0, 3), 3)):
            serviced.privileges.add(choice(privils))
        serviced.save()

        date_of_issue = datetime(year=datetime.now().year - randint(0, 15),
                                 month=date_of_birth.month,
                                 day=date_of_birth.day)
        passport = PassportData(
            serial=randint(1000, 9999),
            number=randint(100000, 999999),
            date_of_issue=date_of_issue,
            serviced_person=serviced
        )
        passport.save()


if __name__ == '__main__':
    from django.core import management
    import os

    management.call_command('flush', '--noinput', '--settings=SocialHouse.settings.dev')
    User.objects.create_superuser('admin', 'admin@mail.com', 'qwerty')
    # print(os.path.abspath(os.path.curdir))

    management.call_command('services_import', '--file=..\source_data\services.xlsx',
                            '--settings=SocialHouse.settings.dev')
    #
    print("Filing random data")
    print("Fill privileges")
    generate_privileges()

    print("Fill normal serviced")
    generate_serviced(26)

    print("Fill sick serviced")
    generate_serviced(2, location=ServicedPerson.STATUSES[1][0])
    print("Fill travel serviced")
    generate_serviced(2, location=ServicedPerson.STATUSES[2][0])
    print("Fill dead serviced")
    generate_serviced(6, dead=True)
    print("Fill leaved serviced")
    generate_serviced(3, left=True)
    cnt_ippsu = 0
    for ippsu in create_and_fill_IPPSU_serviced_workers():
        cnt_ippsu += 1
        print(f"Fill IPPSU #{cnt_ippsu} - {ippsu}")
        create_and_fill_provided_services(ippsu,
                                          date_from=datetime.now().date() - timedelta(days=28),
                                          date_to=datetime.now().date())
