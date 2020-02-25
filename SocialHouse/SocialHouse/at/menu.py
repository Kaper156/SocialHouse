from django.urls import reverse
from admin_tools.menu import items, Menu


class SocialHouseMenu(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem("Административная панель", reverse('admin:index')),
            items.Bookmarks(title="Закладки"),
            items.AppList(
                "По приложениям",
                exclude=('django.contrib.*',)
            ),
            items.AppList(
                "Системное",
                models=('django.contrib.*',)
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(SocialHouseMenu, self).init_with_context(context)
