from django.urls import reverse
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class SocialHouseIndexDashboard(Dashboard):
    columns = 2
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            "Быстрый доступ",
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                ["Перейти на сайт отделения", '/'],
                ["Выйти из учётной записи", reverse('%s:logout' % site_name)],
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            "Приложения",
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            "Системное",
            models=('django.contrib.*',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions("Последние действия", 5))


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
