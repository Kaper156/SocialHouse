from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name
from django.urls import reverse

from SocialHouse.at.applist import receptionist_models, persons_models, department, social_work, \
    documentation


class SocialHouseIndexDashboard(Dashboard):
    columns = 2
    title = "Административная панель"

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        self.children.append(modules.LinkList(
            "Быстрый доступ",
            layout='inline',
            draggable=True,
            deletable=False,
            collapsible=False,
            children=[
                ["Перейти на сайт отделения", '/'],
                ["Выйти из учётной записи", reverse('%s:logout' % site_name)],
            ]
        ))
        self.children.append(modules.Group(
            title="Личные дела",
            display="tabs",
            children=[
                modules.AppList(title=title, models=models) for title, models in persons_models.items()
            ]
        ))
        self.children.append(modules.Group(
            title="Отделение и внешние даннные",
            display="tabs",
            children=[
                modules.AppList(title=title, models=models) for title, models in department.items()
            ]
        ))
        self.children.append(modules.Group(
            title="Социальная работа",
            display="tabs",
            children=[
                modules.AppList(title=title, models=models) for title, models in social_work.items()
            ]
        ))

        self.children.append(modules.Group(
            title="Документация",
            display="tabs",
            children=[
                modules.AppList(title=title, models=models) for title, models in documentation.items()
            ]
        ))
        #
        # self.children.append(modules.Group(
        #     title="Данные",
        #     display="tabs",
        #     children=[
        #         modules.AppList(title=title, models=models) for title, models in all_models.items()
        #     ]
        # ))
        self.children.append(modules.Group(
            title="Работа администратора",
            display="tabs",
            children=[
                modules.AppList(title=title, models=models) for title, models in receptionist_models.items()
            ]
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            "Системное",
            models=('django.contrib.*',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions("Последние действия", 15))


class SocialHouseAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for SocialHouseOnDjango.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                "Быстрый доступ",
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(SocialHouseAppIndexDashboard, self).init_with_context(context)
