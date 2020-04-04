def clone(instance, model, count=1, update_dict=None):
    kwargs = {key: value for key, value in instance.__dict__.items() if not key.startswith('_')}
    kwargs['id'] = None
    if update_dict:
        kwargs.update(update_dict)
    return list(map(lambda _: model(**kwargs), range(count)))


def clone_and_save_without_signals(instance, model, **kwargs):
    return model.objects.bulk_create(
        clone(instance, model, **kwargs)
    )


def force_save(model, instances):
    return model.objects.bulk_create(
        instances
    )
