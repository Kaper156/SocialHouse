from django import template

register = template.Library()


def get_all_fields(obj):
    """Returns a list of all field names on the instance."""
    fields = dict()
    for f in obj._meta.fields:
        fname = f.name
        get_choice = 'get_' + fname + '_display'
        if hasattr(obj, get_choice):
            value = getattr(obj, get_choice)()
        else:
            try:
                value = getattr(obj, fname)
            except AttributeError:
                value = None

        # only display fields with values and skip some fields entirely
        if f.editable and value and f.name not in ('id',):
            fields[f.verbose_name] = value
    return fields


@register.inclusion_tag('_display_object/display_object.html', takes_context=False)
def display_object(obj):
    return {"obj_fields": get_all_fields(obj)}
