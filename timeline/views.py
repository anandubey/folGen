from django.shortcuts import redirect
from django.contrib import messages
from .timeline_functions import timeline, create_new_post
from user.models import User
# Timeline views


def index(request):
    logged = request.session.get('logged')
    if not logged:
        messages.info(request, '1')
        return redirect('home')
    else:
        
        if request.method == 'GET':
            return timeline(request)
        else:
            text = request.POST.get('post_content')
            if text is None or set(text) == {''} or len(text) == 0:
                return redirect('timeline')
            active_user = request.session.get('username')
            create_new_post(active_user, text)
            return timeline(request)

