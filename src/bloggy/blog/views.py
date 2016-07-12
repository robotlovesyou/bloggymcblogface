from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return HttpResponse("Index.")


@login_required
def admin(request):
    return HttpResponse("Admin.")


def admin_login(request):
    all_messages = messages.get_messages(request)
    errors = [m for m in all_messages if m.level == messages.ERROR]

    return render(request, "blog/login.html", {'errors': errors})


def admin_do_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('blog:admin'))

    messages.error(request, 'Username and/or password not recognised')

    return HttpResponseRedirect(reverse('blog:login'))


def article(request, article_id):
    return HttpResponse("Article %s." % article_id)
