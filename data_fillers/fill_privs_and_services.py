if __name__ == '__main__':
    from data_fillers.helpers import *

    flush_db()
    load_services()
    generate_privileges()
