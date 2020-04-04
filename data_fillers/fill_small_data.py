if __name__ == '__main__':
    from data_fillers.helpers import *

    only_active_serviced = True
    create_superuser()
    exit()
    flush_db()
    try:
        try_load_fixture()
    except Exception as e:
        print("something went wrong:%s" % e)
        load_services()
        generate_privileges()
    add_random_limits()
    print("Fill normal serviced")
    generate_serviced(1)
    if not only_active_serviced:
        print("Fill sick serviced")
        generate_serviced(1, location=ServicedPerson.STATUSES[1][0])
        print("Fill travel serviced")
        generate_serviced(1, location=ServicedPerson.STATUSES[2][0])
        print("Fill dead serviced")
        generate_serviced(1, dead=True)
        print("Fill leaved serviced")
        generate_serviced(1, left=True)
    else:
        print("Skip filling sick, travel, dead, and moved serviced")
    cnt_ippsu = 0
    for ippsu in create_and_fill_IPPSU_serviced_workers(cnt_workers=1):
        cnt_ippsu += 1
        print(f"Fill IPPSU #{cnt_ippsu} - {ippsu}")
        create_and_fill_provided_services(ippsu,
                                          date_from=datetime.now().date() - timedelta(days=28),
                                          date_to=datetime.now().date())
