import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialHouse.settings.dev')

import django

django.setup()

from datetime import datetime, timedelta
from random import randint, choice

from faker import Faker

from django.core import management

from applications.department.income_data.models import LivingWage, AveragePerCapitaIncome
from applications.department.general_data.models import DepartmentInfo

from applications.documentation.acts.models import SocialAct
from applications.department.people.models import ServicedPerson, User, Worker, WorkerPosition
from applications.department.people_data.models.serviced_data import PassportData, Privilege, PrivilegeCertificate

from applications.social_work.services.enums import ServiceTypeEnum
from applications.department.people.enums import WorkerPositionEnum
from utils.datetime import range_month, random_date_between
from applications.social_work.services.models import ServicesList, Service
from applications.social_work.providing.models import ProvidedJournal, ProvidedService
from applications.documentation.contracts.models import IPPSU, SocialContract, PaidContract

from applications.social_work.limitations.enums import PeriodEnum
from applications.social_work.limitations.models import PeriodLimitation, VolumeLimitation

from django.conf import settings  # correct way

base_dir = settings.BASE_DIR
APPLICATIONS_FOLDER_PATH = os.path.join(base_dir, 'applications')
faker = Faker(locale='ru_RU')
PASSWORD_FOR_TEST_USERS = 'aq12wsde3'


def get_department_info():
    return DepartmentInfo.objects.get_or_create(
        # department_chief=WorkerPosition.objects.filter(position=WorkerPositionEnum.CHIEF).first(),
        department_title="отделение социального обслуживания на дому граждан пожилого возраста, "
                         "проживающих в домах муниципального специализированного жилищного фонда, "
                         "для социальной защиты отдельных категорий граждан",
        department_title_short="отделение социального обслуживания на дому граждан пожилого возраста, "
                               "проживающих в домах муниципального специализированного жилищного фонда, "
                               "для социальной защиты отдельных категорий граждан",

        department_address="р.п. Тевриз, ул. Кирова 1а",

        department_address_region="Тевризский",
        department_address_city="Тевриз",
        department_address_street="Кирова",
        department_address_house="1а",

        department_rooms=42,
        department_floors=2,

        kcson_chief="Ольга Васильевна КЦСОНовна",
        kcson_chief_short="О.В. КЦСОНовна",
        kcson_title="комплексный центр социального обслуживания населения Тевризского района",
        kcson_title_short="КЦСОН Тевризского района",

    )[0]


def generate_privileges():
    print("Add standard privileges")
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
    worker = worker or generate_worker(Worker.STATUSES[1][0])

    date_of_appointment = faker.date_of_birth(tzinfo=None, minimum_age=1, maximum_age=5)

    worker_position = WorkerPosition.objects.get_or_create(
        worker=worker,
        position=position,
        date_of_appointment=date_of_appointment,
        rate=1,
        department=get_department_info()
    )[0]

    if is_dismiss:
        worker_position.dismissal_date = datetime.now().date() - timedelta(days=randint(1, 180))
        worker.status = Worker.STATUSES[0][0]
        worker.save()
    worker_position.save()
    return worker_position


def get_all_services():
    return ServicesList.objects.last().service_set.all()


def create_included_services(ippsu, cnt=30):
    # not_included_services = get_all_services().by_type.guaranteed()
    not_included_services = Service.by_type.guaranteed().filter(services_list=ServicesList.objects.last())
    while cnt:
        service = choice(not_included_services)
        ippsu.included_services.add(service)
        ippsu.save()
        not_included_services = not_included_services.exclude(pk=service.pk)
        cnt -= 1


def generate_IPPSU(serviced_person, social_worker, date_from, date_to=None, cnt_included=30):
    ippsu = IPPSU.objects.get_or_create(
        serviced_person=serviced_person,
        executor=social_worker,
        date_from=date_from,
        department_info=get_department_info()
    )[0]
    if date_to:
        ippsu.date_expiration = date_to
    ippsu.save()

    create_included_services(ippsu=ippsu, cnt=cnt_included)
    return ippsu


def generate_contract_social(serviced_person, social_worker, date_from):
    contract = SocialContract.objects.get_or_create(
        serviced_person=serviced_person,
        executor=social_worker,
        date_from=date_from,
        serial_number=str(randint(10000, 99999)),
        department_info=get_department_info()
    )[0]
    contract.save()
    return contract


def generate_contract_paid(serviced_person, social_worker, date_from):
    contract = PaidContract.objects.get_or_create(
        serviced_person=serviced_person,
        executor=social_worker,
        date_from=date_from,
        serial_number=str(randint(10000, 99999)),
        department_info=get_department_info()
    )[0]
    contract.save()
    return contract


def create_and_fill_contracts_serviced_workers(cnt_workers=3):
    # cnt_workers = 3
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
            contract_social = generate_contract_social(serviced_person, social_worker=worker_position,
                                                       date_from=date_from)
            contract_paid = generate_contract_paid(serviced_person, social_worker=worker_position, date_from=date_from)
            yield ippsu, contract_social, contract_paid


def pop_random_obj_from_q(queryset):
    random_obj = choice(queryset)
    queryset.exclude(pk=random_obj.id)
    return random_obj, queryset


def generate_provided_service(journal, service, date1, date2):
    date_of = random_date_between(date1, date2)
    volume = 1
    if service.volume_limitation:
        volume = randint(1, service.volume_limitation.limit * 2)
    quantity = 1
    if service.period_limitation:
        quantity = randint(1, service.period_limitation.limit * 2)
        # volume = randint(1, service.volume_statement.measurement.volume_statement.limit * 2)
    # quantity = randint(1, service.measurement.period_statement.limit * 2)
    fields = {
        'journal': journal,
        'date_of': date_of,
        'service': service,
        'volume': volume,
        'quantity': quantity,
    }

    provided_service = ProvidedService.objects.filter(**fields)
    if provided_service.exists():
        provided_service = provided_service.first()
    else:
        provided_service = ProvidedService.objects.get_or_create(**fields)[0]
        provided_service.save()
    print(f"\t\t{provided_service}")


def create_and_fill_provided_services(ippsu, contract_social, contract_paid, date_from=None, date_to=None, g_count=None,
                                      a_count=None, p_count=None):
    # for contracts in IPPSU.objects.filter(is_archived=False):
    # TODO for many months
    # Be careful create only first and last month journal
    date_range = {range_month(date_from), range_month(date_to)}
    journals = list()
    for date1, date2 in date_range:

        journal = ProvidedJournal.objects.get_or_create(
            ippsu=ippsu,
            date_from=date1,
            date_to=date2,
            contract_social=contract_social,
            contract_paid=contract_paid,
        )[0]

        # TODO Add it as manager
        guaranteed = ippsu.included_services.all()
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
        print(f"\tAdd provided journal #{journal.id}_{journal.period()} to {journal.ippsu}")
        journals.append(journal)
    return journals


def generate_social_act(journal: ProvidedJournal,
                        living_wage: LivingWage = None, avg: AveragePerCapitaIncome = None,
                        living_tax=6000, avg_tax=5000):
    date_before = journal.date_from - timedelta(days=90)
    living_wage = living_wage or LivingWage.objects.get_or_create(tax=living_tax,
                                                                  date_to=date_before)[0]

    avg = avg or AveragePerCapitaIncome.objects.get_or_create(
        serviced_person=journal.ippsu.serviced_person,
        date_to=date_before,
        avg_income=avg_tax
    )[0]
    return SocialAct.objects.get_or_create(
        living_wage=living_wage,
        avg_per_capita_income=avg,
        journal=journal,
    )[0]


PICKED_ROOMS = list()


def generate_room_and_floor():
    dep = get_department_info()
    room = randint(0, dep.department_rooms)
    while room in PICKED_ROOMS:
        room = randint(0, dep.department_rooms)
        print(f"        Try pick: {room}")
    PICKED_ROOMS.append(room)
    floor = (room // (dep.department_rooms // dep.department_floors)) + 1
    return room, floor


def generate_serviced(N=30, dead=False, left=False, location=None):
    privils = Privilege.objects.all()
    result = list()
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
        contract_number = f"№{randint(10, 99)}/{randint(10, 99)}"
        date_of_income = faker.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=2)

        date_of_issue = datetime(year=datetime.now().year - randint(0, 15),
                                 month=date_of_birth.month,
                                 day=date_of_birth.day)

        serviced = ServicedPerson(
            name=name,
            patronymic=patronymic,
            surname=surname,
            gender=gender,
            date_of_birth=date_of_birth,
            # contract_number=contract_number,
            date_of_income=date_of_income,
            # passport_data=passport
        )

        if dead:
            serviced.date_of_death = faker.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=3)
        if left:
            serviced.date_of_departure = faker.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=3)
        if location:
            serviced.location = location
        serviced.room, serviced.floor = generate_room_and_floor()
        print(f"        Pick: {serviced.address_in_department()}")
        serviced.save()

        passport = PassportData.objects.get_or_create(
            issued_authority="ОВД Тевризского района Омской области",
            serviced_person=serviced
        )[0]
        for _ in range(randint(randint(0, 3), 3)):
            # TODO changed privilege
            # serviced.privileges.add(choice(privils))
            cert = PrivilegeCertificate.objects.get_or_create(privilege=choice(privils), serviced_person=serviced,
                                                              date_of=faker.date_of_birth(tzinfo=None, minimum_age=0,
                                                                                          maximum_age=5))
            # serviced.privileges.add()
        serviced.save()

        passport.save()
        result.append(serviced)
    return result


def set_limits(service, volume_limit, period_limit=0, period_type=None):
    if volume_limit:
        volume_limitation = VolumeLimitation.objects.get_or_create(limit=volume_limit)[0]
        volume_limitation.save()
        service.volume_limitation = volume_limitation
    if period_limit:
        period_limitation = PeriodLimitation.objects.get_or_create(limit=period_limit, period=period_type)[0]
        period_limitation.save()
        service.period_limitation = period_limitation
    return service


def add_random_limits():
    print("Add random limits by period and volume to services")
    all_services = get_all_services()
    guaranteed = all_services.filter(type_of_service=ServiceTypeEnum.GUARANTEED)
    period_choices = [0] * 10 + list(range(1, 5))
    volume_choices = [0] * 10 + list(range(10, 100, 10))
    period_type_choices = PeriodEnum.values
    period_type_choices.remove(None)
    for g in guaranteed:
        set_limits(
            service=g,
            volume_limit=choice(volume_choices),
            period_limit=choice(period_choices),
            period_type=choice(period_type_choices),
        ).save()
    for other in all_services.exclude(type_of_service=ServiceTypeEnum.GUARANTEED):
        set_limits(
            service=other,
            volume_limit=choice(volume_choices),
            # period_limit=choice(period_choices),
            # period_type=choice(PeriodEnum.values),
        ).save()


def create_superuser(login='admin', mail='admin@mail.com', password='qwerty'):
    User.objects.create_superuser(login, mail, password)
    print("Erase DB ended, created superuser:\nadmin: qwerty")


def flush_db(create_admin=True):
    print("Erase DB started")
    management.call_command('flush', '--noinput', '--settings=SocialHouse.settings.dev')
    if create_admin:
        create_superuser()


def try_load_fixture(fixture_path=''):
    print("Trying to load data from fixture")
    fixture_path = fixture_path or 'services_privs_and_standart_volume_limit.json'
    management.call_command('loaddata', fixture_path)


def load_services():
    srvs_xlsx = '..\source_data\services.xlsx'
    print("Loading services from %s" % srvs_xlsx)
    management.call_command('services_import', '--file=' + srvs_xlsx,
                            '--settings=SocialHouse.settings.dev')


def do_in_dir(func, path):
    def wrapper(*args, **kwargs):
        temp_path = os.path.abspath(os.curdir)
        print(f"CurDir: {temp_path}")
        os.chdir(path)
        print(f"Changed to: {os.path.abspath(os.curdir)}")
        result = func(*args, **kwargs)
        os.chdir(temp_path)
        print(f"Return to: {os.path.abspath(os.curdir)}")
        return result

    return wrapper
