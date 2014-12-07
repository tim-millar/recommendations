"""
A delicious link recommender using the delicious API.
"""

from pydelicious import get_popular, get_userposts, get_urlposts
from collections import defaultdict

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

