from django.db import models
from applications.core.models import Worker

from applications.core.utils.slug import slugify

NEWS_STATUS = (
    ('A', "Опубликована"),
    ('W', "Черновик"),
    ('D', "Удалена"),

)


# TODO rename to POST
class News(models.Model):
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    author = models.ForeignKey(Worker, on_delete=models.SET_NULL, verbose_name="Автор", null=True)
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    date_of_creation = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    date_of_update = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    status = models.CharField(verbose_name="Статус", choices=NEWS_STATUS, max_length=1, default=NEWS_STATUS[1][0])
    slug_url = models.SlugField(max_length=350, unique=True, verbose_name="URL", editable=False)

    def __str__(self):
        return f"[{self.date_of_creation}] {self.title}"

    def save(self, *args, **kwargs):
        self.slug_url = slugify(self.title)
        try:
            q = News.objects.filter(slug_url__iexact=self.slug_url)
            if q.count():
                self.slug_url += f'-{q.count() + 1}'
                # self.slug_url += f'{self.date_of_creation.strftime("__%Y_%B_%d_%H-%M-%S")}'
        except News.DoesNotExist:
            pass
        super(News, self).save(*args, **kwargs)
