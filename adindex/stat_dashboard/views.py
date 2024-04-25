from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # print('smss')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                # login(request)
                return redirect('/dashboard')  # Перенаправление на главную страницу после успешного входа
            else:
                form.add_error(None, "Неверное имя пользователя или пароль.")
    else:
        form = LoginForm()
    # return render(request, 'login.html', {'form': form})
    return render(request, "stat_dashboard/login.html",{'form': form})

def dashboard(request):
    return render(request, "stat_dashboard/dashboard.html",)