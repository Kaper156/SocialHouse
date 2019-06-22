from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def index(req):
    return render(request=req, template_name='index.html')


@login_required
def profile(req):
    from .models import Worker, WorkerPosition
    context = dict()
    context['worker'] = Worker.objects.get(user__username='admin')
    context['worker_positions'] = WorkerPosition.objects.filter(worker=context['worker'])
    return render(request=req, template_name='core/profile.html', context=context)
