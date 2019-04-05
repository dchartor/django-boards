from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        f = SignUpForm(request.POST)
        if f.is_valid():
            user = f.save()
            login(request, user)
            return redirect('boards:home')
    else:
        f = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': f})


def logout_view(request):
    logout(request)
    return redirect('boards:home')
