from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def get_current_user(request):
    if request.user.is_authenticated:
        return request.user
    else:
        return User.objects.get(username='guest')
