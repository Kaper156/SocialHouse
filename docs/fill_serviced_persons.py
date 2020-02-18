import os
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialHouse.settings.dev')
import django

from faker import Faker
from random import randint, choice

django.setup()
from applications.core.models import ServicedPerson, Privilege, PassportData

faker = Faker(locale='ru_RU')


def generate_serviced(N=30, dead=False, leaved=False, location=None):
    privils = Privilege.objects.all()
    for i in range(N):
        name, patronymic, surname = '', '', ''
        if randint(1, 10) % 2:
            # Male
            gender = 'M'
            name = faker.first_name_male()
            patronymic = faker.middle_name()
            surname = faker.last_name_male()
        else:
            # Female
            gender = 'F'
            name = faker.first_name_female()
            patronymic = faker.middle_name()
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
        if leaved:
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
    print("Filling random data")
    generate_serviced(26)
    generate_serviced(2, location=ServicedPerson.STATUSES[1][0])
    generate_serviced(2, location=ServicedPerson.STATUSES[2][0])
    generate_serviced(6, dead=True)
    generate_serviced(3, leaved=True)

    print("Filling done ")
