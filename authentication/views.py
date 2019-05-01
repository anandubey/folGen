from django.shortcuts import render, redirect
from django.contrib import messages
from .custom import *
from .models import Credential
from user.models import User
from user.models import Deleted_UID


def index(request):
    logged = request.session.get('logged')
    if not logged:
        if request.method == 'POST':
            if authenticate(request):
                login(request)
                return redirect('timeline')
            else:
                return render(request, 'authentication/index.html', {'wrongcredential': True})
        else:
            return render(request, 'authentication/index.html', {})
    else:
        return redirect('timeline')


def logout_user(request):
    logout(request)
    return redirect('home')


def signup(request):
    form = request.POST
    email = form['email']
    name = form['name']
    username = form['username']
    password = form['signup_password']
    conf_password = form['signup_confirm_password']

    try:
        User.objects.get(username=username)
        print("ERROR! Username is already in use.")
        return redirect('home')
    except:
        try:
            User.objects.get(email=email)
            print("ERROR! Email ID is already in use.")
            return redirect('home')
        except:
            print("All good!")
    active_unique_id_list = list(User.objects.values_list('unique_id'))
    deleted_unique_id_list = list(Deleted_UID.objects.values_list('unique_id'))
    unique_id = get_unique_id(deleted_unique_id_list, active_unique_id_list)

    if password == conf_password:
        new_user = User.objects.create(username=username, name=name, email=email, followers='', following='', unique_id=unique_id)
        new_user.save()
        print("user saved")
        try:
            deleted_uid = Deleted_UID.objects.get(unique_id=unique_id)
            if deleted_uid is not None:
                deleted_uid.delete()
        except:
            print("except block")
        password = get_hash(password, unique_id)
        new_user_cred = Credential.objects.create(username=new_user, password_hash=password)
        new_user_cred.save()
        print("cred saved")

        messages.info(request, '3')
        return redirect('home')
    else:
        messages.info(request, '4')
        return redirect('home')

