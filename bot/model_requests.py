import requests
from cfg import BOT_CFG


def get_url(suffix):
    return BOT_CFG['prefix_apply_to'] + suffix


def request_total_posts(user):
    headers = {
        "Authorization": f"Bearer {user.token}",
    }
    return requests.get(get_url("/liker/posts/"), headers=headers)


def singup_user(user):

    headers = {"Content-Type": "application/json"}
    return requests.post(
        get_url("/liker/users/singup/"), data=user.signup_data(), headers=headers
    )


# /liker/users/token/


def login_user(user):
    return requests.post(
        get_url("/liker/users/token/"), auth=(user.username, user.password)
    )


def create_post(user):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user.token}",
    }
    return requests.post(
        get_url("/liker/posts/"), data=user.creativity(), headers=headers
    )


def like_post(user, post_id):
    headers = {
        "Authorization": f"Bearer {user.token}",
    }
    return requests.post(get_url(f"/liker/posts/{post_id}/like/"), headers=headers)
