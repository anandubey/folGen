from .models import Post
from user.models import User
from datetime import datetime
from django.shortcuts import render


def create_new_post(current_user, post_content):
    user_instance = User.objects.get(username=current_user)
    active_uid = user_instance.unique_id
    timestamp = int(datetime.now().timestamp())                 # Using epoch time
    post_id = str(active_uid) + '-' + str(timestamp)
    new_post = Post(post_id=post_id, post_content=post_content, liked_by='')
    new_post.save()
    return


def timeline(request):
    username = request.session.get('username')
    user_obj = User.objects.get(username=username)
    posts = []
    try:
        posts = sorted(post_generator(request).items(), reverse=True)
    
    except:
        posts = []
    print(posts[0])
    return render(request, 'timeline/timeline.html', {'posts': posts, 'user_data':user_obj})


def post_generator(request):
    active_user = request.session.get('username')
    user_instance = User.objects.get(username=active_user)
    active_uid = user_instance.unique_id
    following_list = [active_uid]

    if len(user_instance.following) != 0:
        following_list += user_instance.following.split('-')
    following_list.sort()

    post_dict = {}
    for uid in following_list:
        user_ins = User.objects.get(unique_id=uid)
        post_dict = __post_by_user(post_dict, unique_id=uid, name=user_ins.name, username=user_ins.username)

    return post_dict


def __post_by_user(post_dict, unique_id='', name='', username=''):
    posts = Post.objects.filter(post_id__istartswith=unique_id)
    if posts is not None:
        for post in posts:
            timestamp = int(post.post_id[4:])
            human_time = datetime.fromtimestamp(timestamp).strftime('%d:%b:%Y %I:%M %p')
            content = post.post_content
            if post_dict.get(timestamp) is not None:
                post_dict[timestamp].append({'time': human_time, 'name': name, 'text': content, 'username': username})
            else:
                post_dict[timestamp] = [{'time': human_time, 'name': name, 'text': content, 'username': username}]
        return post_dict
        # retrieve posts by given user
    else:
        return None  # if user had not written any post

