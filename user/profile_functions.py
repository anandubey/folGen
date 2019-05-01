from user.models import User
from timeline.models import Post
from datetime import datetime


def user_data(request):
    my_username = request.session.get('username')
    my_instance = User.objects.get(username=my_username)
    my_uid = my_instance.unique_id
    my_name = my_instance.name
    my_email = my_instance.email
    my_followers = my_instance.followers
    my_following = my_instance.following
    self_data = {'name': my_name, 'email': my_email, 'username': my_username}
    my_posts = post_by_user(my_uid)

    followers_list = []
    following_list = []
    if len(my_followers) != 0:
        followers_uid_list = my_followers.split('-')
        followers_list = users_name_list(followers_uid_list)

    if len(my_following) != 0:
        following_uid_list = my_following.split('-')
        following_list = users_name_list(following_uid_list)

    liked_posts = liked_posts_list(my_uid)
    return {'self_data': self_data, 'posts': my_posts, 'followers': followers_list, 'following': following_list, 'liked_posts': liked_posts}


def users_name_list(uid_list=None):
    if uid_list is None:
        return None
    names_list = []
    for uid in uid_list:
        user_instance = User.objects.get(unique_id=uid)
        name = user_instance.name
        username = user_instance.username
        names_list.append({'name': name, 'username': username})
    return names_list


def liked_posts_list(uid):
    posts_liked = Post.objects.filter(liked_by__contains=uid)
    print(type(posts_liked))
    liked_posts = []
    for post in posts_liked:
        content = post.post_content
        posting_uid = post.post_id[0:3]
        post_time = post.post_id[4:]
        timestamp = datetime.fromtimestamp(int(post_time)).strftime('%d:%b:%Y %I:%M %p')
        posted_by = User.objects.get(unique_id=posting_uid).name
        liked_posts.append({'content': content, 'posted_by': posted_by, 'timestamp': timestamp})
    return liked_posts


def post_by_user(unique_id=None):
    if unique_id is None:
        return None
    posts = Post.objects.filter(post_id__istartswith=unique_id)
    posts_list = []
    if posts is not None:
        for post in posts:
            timestamp = int(post.post_id[4:])
            human_time = datetime.fromtimestamp(timestamp).strftime('%d:%b:%Y %I:%M %p')
            content = post.post_content
            posts_list.append({'content': content, 'timestamp': human_time})
        return posts_list
        # retrieve posts by given user
    else:
        print("no posts")
        return None  # if user had not written any post