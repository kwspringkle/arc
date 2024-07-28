from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('log:home_page')
        else:
            context = {'form': form, 'error': 'Invalid username or password'}
            return render(request, 'login.html', context)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view (request):
    return redirect('log:login_page')

@login_required
def render_home(request):
    return render(request, 'home.html')

def render_login(request):
    logout(request)
    return render(request, 'login.html')