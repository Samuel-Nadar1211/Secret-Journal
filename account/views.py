from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .forms import UserForm

# Create your views here.
def index (request):
    if 'user_id' in request.COOKIES or 'password' in request.COOKIES:
        return redirect ('entry:home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']

        try:
            user = User.objects.get (email = email)

            if not check_password(password, user.password):
                return render (request, 'index.html', { "message" : "Incorrect Password" })
            
            response = redirect ('entry:home')
            response.set_cookie ('user_id', user.user_id, max_age = 3600, httponly = True)
            response.set_cookie ('password', user.password, max_age = 3600, httponly = True)
            return response

        except User.DoesNotExist:
            return render (request, 'index.html', { "message" : "Email does not exist" })

    return render (request, 'index.html', { "message" : None })


def register (request):
    if request.method == 'POST':
        form = UserForm (request.POST)
        if form.is_valid():
            user = form.save (commit = False)
            user.password = make_password (form.cleaned_data['password'])
            user.save()
            return redirect('account:index')
    else:
        form = UserForm()

    return render (request, 'register.html', { "form" : form })


def logout (request):
    response = redirect ('account:index')

    if 'user_id' in request.COOKIES:
        response.delete_cookie('user_id')
    
    if 'password' in request.COOKIES:
        response.delete_cookie('password')

    return response