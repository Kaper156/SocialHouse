from scripts.helpers import *

if __name__ == '__main__':

    flush_db()
    load_services()
    add_random_limits()
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
    print("Generate chief of department")
    generate_worker_position(position=WorkerPositionEnum.CHIEF)
    for ippsu, contract_social, contract_paid in create_and_fill_contracts_serviced_workers():
        cnt_ippsu += 1
        print(f"Fill IPPSU #{cnt_ippsu} - {ippsu}")
        create_and_fill_provided_services(ippsu, contract_social, contract_paid,
                                          date_from=datetime.now().date() - timedelta(days=28),
                                          date_to=datetime.now().date()
                                          # date_from=datetime(2020, 1, 1),
                                          # date_to=datetime(2020, 2, 31)
                                          )
