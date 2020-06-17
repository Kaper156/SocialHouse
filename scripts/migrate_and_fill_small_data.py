from scripts.fill_small_data import main
from scripts.helpers import *


def main_migrate_and_fill_small_data():
    # call_in_root = do_in_dir(management.call_command, '../SocialHouse')
    management.call_command('makemigrations')
    management.call_command('migrate')
    main()


if __name__ == '__main__':
    main_migrate_and_fill_small_data()
