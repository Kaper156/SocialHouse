from datetime import datetime
from decimal import Decimal

import xlrd

from applications.social_work.services.enums import ServiceTypeEnum
from applications.social_work.services.models import ServiceMeasurement, ServicesList, Service


class Loader:
    def __init__(self, file_path):
        self.xl = xlrd.open_workbook(file_path)
        print(f"Open spreadsheet at '{file_path}'")
        self.services_list = ServicesList.objects.get_or_create(date_from=datetime.now().date())[0]
        self.services_list.save()

    def load_guaranteed(self):
        sheet = self.xl.sheet_by_index(0)
        pre1 = ''
        category = ''

        # Make dict, where keys is description and values is keeped in db values
        categories = {key.lower(): value for value, key in Service.SERVICE_CATEGORIES}

        for row in sheet.get_rows():
            if len(row[0].value) > 5:
                category_name = row[0].value.split('.', 1)[1].lower().strip()
                category = categories.get(category_name, 'OT')
                continue
            title = row[1].value
            if not (row[2].value and row[3].value):
                pre1 = title
                continue
            if '.' in row[0].value or ',' in row[0].value:
                title = ' '.join((pre1, title))
            measurement = self._get_measurement_(row[2].value)
            tax = row[3].value.replace(',', '.')
            tax = Decimal(tax)
            yield Service(
                title=' '.join(title.split()),
                type_of_service=ServiceTypeEnum.GUARANTEED,
                service_category=category,
                measurement=measurement,
                tax=tax,
                services_list=self.services_list
            )

    def load_additional(self):
        sheet = self.xl.sheet_by_index(1)
        pre1 = ''
        category = ''

        # Make dict, where keys is description and values is keeped in db values
        categories = {key.lower(): value for value, key in Service.SERVICE_CATEGORIES}

        for row in sheet.get_rows():
            if row[0].value is str and len(row[0].value) > 5:
                category_name = row[0].value.split('.', 1)[1].lower().strip()
                category = categories.get(category_name, 'OT')
                continue
            title = row[1].value
            if not (row[2].value and row[3].value):
                pre1 = title
                continue
            if row[1].value.strip().startswith('—'):
                title = ' '.join((pre1, title.strip().replace('—', '')))
            measurement = self._get_measurement_(row[2].value)
            tax = row[3].value.replace(',', '.')
            tax = Decimal(tax)
            place = Service.PLACES[0][0]  # Always 'at home'
            yield Service(
                title=' '.join(title.split()),
                type_of_service=ServiceTypeEnum.ADDITIONAL,
                service_category=category,
                measurement=measurement,
                tax=tax,
                services_list=self.services_list,
                place=place
            )

    def load_paid(self):
        sheet = self.xl.sheet_by_index(2)
        pre1 = ''
        pre2 = ''
        splatted_words = 'на дому/в организации'
        for row in sheet.get_rows():
            title = row[1].value
            if not (row[2].value or row[3].value):
                if row[0].value:
                    pre1 = title
                    pre2 = ''
                    continue
                else:
                    pre2 = title
                    continue
            if not row[0].value:
                title = ' '.join((pre1, pre2, title))
            measurement = self._get_measurement_(row[2].value)
            tax = row[3].value.replace(',', '.')

            if '/' in tax:
                titles = [title.replace(splatted_words, half) for half in splatted_words.split('/')]
                taxes = [Decimal(half) for half in tax.split('/')]

                for i in range(2):
                    place = Service.PLACES[i][0]  # select place from choices
                    yield Service(
                        title=' '.join(titles[i].split()),
                        type_of_service=ServiceTypeEnum.PAID,
                        measurement=measurement,
                        tax=taxes[i],
                        services_list=self.services_list,
                        place=place
                    )
            else:
                tax = Decimal(tax)
                yield Service(
                    title=' '.join(title.split()),
                    type_of_service=ServiceTypeEnum.PAID,
                    measurement=measurement,
                    tax=tax,
                    services_list=self.services_list
                )

    def _get_measurement_(self, string):
        return ServiceMeasurement.objects.get_or_create(title=string)[0]

    def load_data(self):
        from itertools import chain
        for service in chain(self.load_guaranteed(), self.load_additional(), self.load_paid()):
            service.save()
