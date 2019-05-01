from django.shortcuts import render, redirect
from django.contrib import messages
from .deletion_functions import *
from .profile_functions import *


def user_profile(request):
    logged = request.session.get('logged')
    if logged:
        profile_data = user_data(request)
        return render(request, 'user/profile.html', profile_data)
    else:
        messages.info(request, '1')
        return redirect('home')


def delete_user(request):
    if not request.session.get('logged'):
        messages.info(request, '1')
        return redirect('home')
    else:
        if request.method == 'POST':
            if verify_deletion_data(request):
                delete_account(request)
                messages.info(request, '5')
                request.session.clear()
                return redirect('home')
            else:
                return render(request, 'user/delete_profile.html', {'wrong_password': True})
        else:
            return render(request, 'user/delete_profile.html')

