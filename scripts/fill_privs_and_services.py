if __name__ == '__main__':
    from scripts.helpers import *

    flush_db()
    load_services()
    generate_privileges()
