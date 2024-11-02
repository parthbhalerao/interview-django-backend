from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def profiles_list_view(request, *args, **kwargs):
    context = {
        "object_list": User.objects.filter(is_active=True),
    }
    return render(request, 'profiles/list.html', context)
    pass

@login_required
def profile_detail_view(request, username=None, *args, **kwargs):
    user = request.user  # current authenticated user
    user_groups = user.groups.all()

    if user_groups.filter(name__icontains='basic').exists():
        return HttpResponse('Congrats! You are a basic user.')
    profile_user_obj = get_object_or_404(User, username=username)
    is_me = profile_user_obj == user
    context = {
        "object": profile_user_obj,
        "instance": profile_user_obj, # same as 'object' for template tag
        "owner": is_me,
    }
    return render(request, 'profiles/details.html', context)

