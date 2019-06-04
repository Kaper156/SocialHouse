from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def index(req):
    return render(request=req, template_name="index.html")


@login_required
def profile(req):
    return redirect(index)

# Create your views here.
