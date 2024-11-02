import pathlib
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from visits.models import PageVisit

LOGIN_URL = settings.LOGIN_URL

this_dir = pathlib.Path(__file__).resolve().parent

def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        print(request.user.first_name)
    return about_view(request, *args, **kwargs)

def about_view(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_qs = qs.filter(path=request.path)

    try:
        percent = round((page_qs.count() / qs.count()) * 100, 2)
    except ZeroDivisionError:
        percent = 0

    my_title = 'About Interview Bot'
    my_context ={
        "page_title": my_title,
        "page_visit_count": page_qs.count(),
        "percent": percent,
        "total_visit_count": qs.count()
    }
    
    html_template = 'home.html'
    PageVisit.objects.create(path=request.path)
    return render(request, html_template, my_context)

def my_old_home_page_view(request, *args, **kwargs):
    my_title = 'Interview Bot'
    my_context ={
        "page_title": my_title,
    }
    html_fp = this_dir / 'home.html'
    html_ = """
    <!DOCTYPE html>
<html>
    <body>
        <h1>Is {page_title} anything?</h1> 
    </body>
</html>
    """.format(**my_context)

    return HttpResponse(html_)

VALID_CODE = 'abc123'
def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0

    if request.method == 'POST':
        user_pw_sent = request.POST.get('code') or None
        if user_pw_sent == VALID_CODE:
            request.session['protected_page_allowed'] = 1

    if is_allowed:
        return render(request, 'protected/view.html', {})
    return render(request, 'protected/entry.html', {})

@login_required
def user_only_view(request, *args, **kwargs):
    return render(request, 'protected/user_only.html', {})

@staff_member_required(login_url=LOGIN_URL)
def staff_only_view(request, *args, **kwargs):
    return render(request, 'protected/user_only.html', {})