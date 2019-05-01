from user.models import User, Deleted_UID
from timeline.models import Post
from authentication.models import Credential
from authentication.custom import get_hash


def delete_account(request):
    username = request.session.get('username')
    user_instance = User.objects.get(username=username)
    credential_instance = Credential.objects.get(username=username)
    current_uid = user_instance.unique_id
    remove_likes(current_uid)
    remove_follows(current_uid)
    delete_posts(current_uid)
    deleted_uid = Deleted_UID(unique_id=current_uid)
    deleted_uid.save()
    credential_instance.delete()
    user_instance.delete()


def verify_deletion_data(request):
    username = request.session.get('username')
    raw_password = request.POST.get('password')
    user_instance = User.objects.get(username=username)
    credential_instance = Credential.objects.get(username=username)
    current_uid = user_instance.unique_id
    saved_password_hash = credential_instance.password_hash
    password_hash = get_hash(raw_password, current_uid)
    if password_hash == saved_password_hash:
        return True
    else:
        return False


def remove_likes(uid):
    liked_posts = Post.objects.filter(liked_by__contains=uid)
    if liked_posts is None:
        return
    for post in liked_posts:
        liked_by = post.liked_by.split('-')
        if uid in liked_by:
            liked_by.remove(uid)
        liked_by = '-'.join(liked_by)
        post.liked_by = liked_by
        post.save()
    return


def remove_follows(uid):
    users_who_follow_me = User.objects.filter(following__contains=uid)
    if users_who_follow_me is None:
        return
    for user in users_who_follow_me:
        following = user.following.split('-')
        followers = user.followers.split('-')
        if uid in following:
            following.remove(uid)
        if uid in followers:
            followers.remove(uid)
        following = '-'.join(following)
        followers = '-'.join(followers)
        user.following = following
        user.followers = followers
        user.save()

    users_followed_by_me = User.objects.filter(followers__contains=uid)
    if users_who_follow_me is None:
        return
    for user in users_followed_by_me:
        followers = user.followers.split('-')
        if uid in followers:
            followers.remove(uid)
        followers = '-'.join(followers)
        user.followers = followers
        user.save()
    return

def delete_posts(uid):
    posts_by_uid = Post.objects.filter(post_id__startswith=uid)
    if posts_by_uid is None:
        return
    else:
        for post in posts_by_uid:
            post.delete()
    return