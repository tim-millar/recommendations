"""
A delicious link recommender using the delicious API.
"""

from pydelicious import get_popular, get_userposts, get_urlposts
from collections import defaultdict
from time import sleep

def initialize_user_dict(tag, count=5):
    """
    Returns: length n dict of users: empty dict pairs.
    """
    user_dict = {}
    for post in get_popular(tag=tag)[:count]:
        for url in get_urlposts(post['url']):
            user = url['user']
            user_dict[user] = {}
    return user_dict

    # user_dict, idx = {}, 0
    # while idx < count:
    #     post = get_popular(tag=tag)[idx]
    #     for url in get_urlposts(post['url']):
    #         user = url['user']
    #         if not user: continue
    #         user_dict[user] = {}
    #         idx += 1
    # return user_dict


def fill_items(user_dict):
    """
    Returns: a dict whose keys are users and values are 
    dicts of link: rating pairs, where 1 stands for having 
    posted the link, else 0.
    """
    all_items = {}
    for user in user_dict:
        for _ in range(3):
            try:
                posts = get_userposts(user)
                break
            except:
                print("Failed user " + user + ", retrying")
                sleep(4)
        for post in posts:
            url = post['url']
            user_dict[user][url] = 1.0
            all_items[url] = 1

    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item] = 0.0

    return all_items
