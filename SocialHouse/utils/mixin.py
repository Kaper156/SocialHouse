from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import admin
from django.shortcuts import redirect
from django.views.generic import TemplateView


class SubmitForm:
    __submit_text__ = 'Сохранить запись'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', self.__submit_text__))
        self.helper.form_class = 'form-horizontal'
        # TODO submit in center
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'


class OneToOneCreateView(TemplateView):
    main_form = None
    sub_form = None
    sub_relation_field = None
    success_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_form'] = kwargs.get('main_form', self.main_form(prefix='main'))
        context['sub_form'] = kwargs.get('sub_form', self.sub_form(prefix='sub'))
        return context

    def form_valid(self, form, form_2):

        main_obj = form.save()

        sub_obj = form_2.save(commit=False)
        setattr(sub_obj, self.sub_relation_field, main_obj)
        sub_obj.save()

        return redirect(self.success_url)

    def form_invalid(self, main_form, sub_form):
        return self.render_to_response(
            self.get_context_data(
                main_form=main_form,
                sub_form=sub_form
            )
        )

    def post(self, request, *args, **kwargs):
        main_form = self.main_form(data=request.POST, prefix='main')
        sub_form = self.sub_form(data=request.POST, prefix='sub')
        if main_form.is_valid() and sub_form.is_valid():
            return self.form_valid(main_form, sub_form)
        else:
            return self.form_invalid(main_form, sub_form)


class YearFilter(admin.SimpleListFilter):
    year_from = 2015
    filtered_parameter = None

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        if not self.filtered_parameter:  # Use parameter name
            self.filtered_parameter = self.parameter_name
        self.filtered_parameter += '__year'  # Add filter-condition

    def lookups(self, request, model_admin):
        return (
            (str(y), y) for y in range(self.year_from, datetime.now().year)
        )

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset
        return queryset.filter(**{self.filtered_parameter: value})