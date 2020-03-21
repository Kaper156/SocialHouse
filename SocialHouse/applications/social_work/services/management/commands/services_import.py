from django.core.management.base import BaseCommand, CommandError

from ._loader_ import Loader


class Command(BaseCommand):
    help = "Provide functonality to load services (with measurement, etc) from xlsx-files"

    __types__ = ("G", "P", "A")

    def add_arguments(self, parser):
        # parser.add_argument('--type', action='store', nargs='+', type=str, required=True, choices=self.__types__)
        parser.add_argument('--file', action='store', nargs='+', type=str, required=True)

    def handle(self, *args, **options):
        loader = None
        # type_of_services = options.get('type', [None])[0]
        filepath = options.get('file', [None])[0]
        if not filepath:
            raise CommandError("Please set path to xlsx file (for ex. --file=./sources/data.xlsx)")
        # try:
        loader = Loader(filepath)
        loader.load_data()
        # except Exception as exc:
        #     raise CommandError("Command error during execution:", exc.args)
