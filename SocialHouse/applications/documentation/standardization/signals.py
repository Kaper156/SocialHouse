import datetime


# All models inherited Document model must be connected with this signal!
def document_pre_save(sender, instance, **kwargs):
    # print("Saving: %s" % instance.get_file_name())
    instance.last_modify = datetime.datetime.now()
    instance.generate_file()
