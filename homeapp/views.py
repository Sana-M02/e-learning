from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm,SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages

@login_required
def home(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    
    if 'learner' in user_groups:
        return redirect('learner')
    elif 'instructor' in user_groups:
        return redirect('instructor')
    elif 'admin' in user_groups:
        return redirect('admin')
    else:
        messages.error(request, 'You do not have a valid group assigned.')
        return redirect('learner')


def login_view(request):
    try:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                # Authenticate user
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    # Login user
                    auth_login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('home')  
                else:
                    messages.error(request, 'Invalid username or password')
            else:
                messages.error(request, 'Invalid form submission')
        else:
            form = LoginForm()
    except Exception as e:
        print(f"An error occurred: {e}")
        messages.error(request, 'An error occurred during login. Please try again later.')

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')


def sign_up(request):
    try:
        if request.method == 'POST':
           form = SignupForm(request.POST)
           if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
           else:
            return render(request, 'sign_up.html', {"form": form})
        else:
          form = SignupForm()
        return render(request, 'sign_up.html', {"form": form})
    
    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred during signup')
        form = SignupForm()
        return render(request, 'sign_up.html', {"form": form})
    
def Resethome(request):
    return render(request,'reset_password.html')

def ResetPassword(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        new_password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successfully.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Username not found.')
            return render(request, 'reset_password.html', {'errormsg': 'Username not found.'})

    return render(request, 'reset_password.html')
       
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dash.html')

@login_required
def instructor_dashboard(request):
    return render(request, 'instructor_dash.html')

@login_required
def learner_dashboard(request):
    return render(request, 'learner_dash.html')
