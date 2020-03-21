from django.shortcuts import render

from .models import News


def news(req):
    context = dict()
    context['posts'] = News.objects.all()
    context['Title'] = "Новости отделения"
    return render(request=req, template_name='news/news.html', context=context)


def post(req, slug_url):
    context = dict()
    context['post'] = News.objects.get(slug_url__iexact=slug_url)
    context['Title'] = context['post'].title
    return render(request=req, template_name='news/post.html', context=context)
