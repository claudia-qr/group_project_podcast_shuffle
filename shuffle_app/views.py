from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    if 'user_id' in request.session:
        return redirect('/home')
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect('/')
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash
            )
        request.session['name'] = new_user.first_name + ' ' + new_user.last_name
        request.session['user_id'] = new_user.id
        return redirect('/home')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        logged_user = User.objects.filter(email=request.POST['email'])
        if len(logged_user) > 0:
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['name'] = logged_user.first_name + ' ' + logged_user.last_name
                request.session['user_id'] = logged_user.id
                return redirect('/home')
    return redirect('/')

def home(request):
    if 'user_id' in request.session:
        logged_user = User.objects.filter(id=request.session['user_id'])
        if len(logged_user) > 0:
            logged_user = logged_user[0]
            if request.session['user_id'] == logged_user.id:
                return render(request, 'home.html')
    return redirect('/')

def account(request, id):
    if 'user_id' in request.session:
        context = {
            'one_user': User.objects.get(id=id)
        }
        return render(request, 'account.html', context)
    return redirect('/')

def editaccount(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            myaccount = User.objects.get(id=request.session['user_id'])
            errors = User.objects.user_validator(request.POST)
            if len(errors) > 0:
                for key, values in errors.items():
                    messages.error(request, values)
                return redirect(f'/account/{str(myaccount.id)}')
            myaccount = User.objects.get(id=request.session['user_id'])
            myaccount.first_name = request.POST['first_name']
            myaccount.last_name = request.POST['last_name']
            myaccount.email = request.POST['email']
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            myaccount.password = pw_hash
            myaccount.save()
            return redirect(f'/account/{str(myaccount.id)}')
    return redirect('/')

def library(request):
    return render(request, 'library.html')

def logout(request):
    request.session.flush()
    return redirect('/')