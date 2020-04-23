from request_queue import Consumer, Task
from model_requests import (
    request_total_posts,
    singup_user,
    login_user,
    create_post,
    like_post,
)
import multiprocessing
from user import User
from cfg import BOT_CFG
import time


def signup_users(users):
    for name, user in users.items():
        tasks.put(Task(singup_user, user, tag="user_signup", user_name=name))

    tasks.join()
    num_jobs = len(users)
    while num_jobs:
        result = results.get()
        print("Result:", num_jobs, result["result"].text)
        if (
            result["result"].status_code == 201
            and result["args"]["tag"] == "user_signup"  # noqa: W503
        ):
            name = result["args"]["user_name"]
            num_jobs -= 1
            users[name].created = True


def login_users(users):
    for name, user in users.items():
        tasks.put(Task(login_user, user, tag="user_login", user_name=name))
    tasks.join()
    num_jobs = len(users)
    while num_jobs:
        result = results.get()
        if (
            result["result"].status_code == 200
            and result["args"]["tag"] == "user_login"  # noqa: W503
        ):
            name = result["args"]["user_name"]
            num_jobs -= 1
            users[name].token = result["result"].json()["access"]
            print(users[name].token)


def get_total_posts(us0):
    tasks.join()
    tasks.put(
        Task(request_total_posts, us0, tag="list_all_posts", user_name=us0.username)
    )
    tasks.join()
    result = results.get()

    total = result["result"].json()
    return len(total), total


def create_posts(users):
    for i in range(BOT_CFG["max_posts_per_user"]):
        for name, user in users.items():
            tasks.put(Task(create_post, user, tag="user_creativity", user_name=name))
    num_jobs = len(users) * BOT_CFG["max_posts_per_user"]
    while num_jobs:
        result = results.get()
        if (
            result["result"].status_code == 201
            and result["args"]["tag"] == "user_creativity"  # noqa: W503
        ):
            name = result["args"]["user_name"]
            num_jobs -= 1


def study_content(users, semantics):
    for _, user in users.items():
        user.enjoy(BOT_CFG["max_likes_per_user"], semantics)


def spurt_activity(users):
    for name, user in users.items():
        for post_id in user.preferences:
            tasks.put(Task(like_post, user, post_id, tag="like_post", user_name=name))

    tasks.join()

    time.sleep(0.7)  # magic
    while not results.empty():
        result = results.get()
        print({"irrelevant": result["result"].text}, result["args"]["user_name"])


if __name__ == "__main__":
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    num_consumers = multiprocessing.cpu_count() * 2
    consumers = [Consumer(tasks, results) for i in range(num_consumers)]
    for w in consumers:
        w.start()

    users_l = [User() for i in range(BOT_CFG["number_of_users"])]
    users = {user.username: user for user in users_l}

    signup_users(users)
    login_users(users)

    before, _ = get_total_posts(users_l[0])

    create_posts(users)

    after, all_posts = get_total_posts(users_l[0])
    assert after - before == BOT_CFG["number_of_users"] * BOT_CFG["max_posts_per_user"]

    semantics = list(map(lambda x: x["id"], all_posts))
    study_content(users, semantics)
    spurt_activity(users)

    for i in range(num_consumers):
        tasks.put(None)
