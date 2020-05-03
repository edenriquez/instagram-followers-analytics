from flask import Flask, request, jsonify
from instapy import InstaPy
from instapy import smart_run
import os
import threading
from threading import Thread
from tasks import threaded_task

app = Flask(__name__)
app.config.from_pyfile('config.py')
insta_username = app.config['USER']
insta_password = app.config['PASS']


@app.route('/follow/<string:username>')
def follow(username):
    thread = Thread(target=follow_user_task, args=(username,))
    thread.daemon = True
    thread.start()
    return jsonify(message=f' User followed  correctly: {username}')


@app.route('/relations/<string:username>')
def get_relations(username):
    thread = Thread(target=relatiohships, args=(username,))
    thread.daemon = True
    thread.start()
    return jsonify(message=f' Checking common followers between accounts: {username}')


def follow_user_task(username):
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=False)
    with smart_run(session, threaded=True):
        try:
            session.login()
            session.follow_by_list(
                followlist=[username],
                times=1,
                sleep_delay=600, interact=False
            )
            session.end(threaded_session=True)
        except:
            session.end(threaded_session=True)
            print('Finishing follow_user_task')


def relatiohships(username):
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=False)
    with smart_run(session, threaded=True):
        try:
            session.login()
            mutual_are_following(session, username)
            session.end(threaded_session=True)
        except:
            session.end(threaded_session=True)
            print('Finishing relathionships')


def mutual_are_following(session, username):
    his_follows = session.grab_following(
        username=username,
        amount="full",
        store_locally=True
    )
    my_follows = session.grab_following(
        username=insta_username,
        amount="full",
        store_locally=True
    )
    mutual_following = [
        follower for follower in his_follows if follower in my_follows
    ]
    print('MUTUAL FOLLOWING', mutual_following)
    return mutual_following


"""
#get followers of "Popeye" and "Cinderella"
user1 = session.grab_following(username="_edd01_mx01", amount="full", live_match=True, store_locally=True)

user2 = session.grab_following(username="_eduardoenriquez", amount="full", live_match=True, store_locally=True)

#find the users following "Popeye" WHO also follow "Cinderella" :D
mutual_are_following = [follower for follower in user1 if follower in user2]

user1 = session.grab_followers(username="_edd01_mx01", amount="full", live_match=True, store_locally=True)
user2 = session.grab_followers(username="_eduardoenriquez", amount="full", live_match=True, store_locally=True)

his_followers_that_follow_you = [follower for follower in user1 if follower in user2]


user1 = session.grab_followers(username="_edd01_mx01", amount="full", live_match=True, store_locally=True)
user2 = session.grab_following(username="_eduardoenriquez", amount="full", live_match=True, store_locally=True)

followers_you_follow_he_follow = [follower for follower in user1 if follower in user2]

user1 = session.grab_followers(username="_edd01_mx01", amount="full", live_match=True, store_locally=True)
user2 = session.grab_followers(username="_eduardoenriquez", amount="full", live_match=True, store_locally=True)

mutual_followers = [follower for follower in user1 if follower in user2]
"""
