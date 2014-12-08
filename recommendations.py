"""
Collaborative filtering and recommendations library
"""

from math import sqrt
from collections import defaultdict

# Dictionary of movies critics and ratings
critics = {
    'Lisa Rose':        {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 
                         'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
    'Gene Seymour':     {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 1.5, 'Superman Returns': 5.0, 
                         'You, Me and Dupree': 3.5, 'The Night Listener': 3.0},
    'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                         'Superman Returns': 3.5, 'The Night Listener': 4.0},
    'Claudia Puig':     {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 
                         'Superman Returns': 4.0, 'You, Me and Dupree': 2.5, 
                         'The Night Listener': 4.5},
    'Mick LaSalle':     {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                         'Just My Luck': 2.0, 'Superman Returns': 3.0, 
                         'You, Me and Dupree': 2.0, 'The Night Listener': 3.0},
    'Jack Matthews':    {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                         'Superman Returns': 5.0, 'You, Me and Dupree': 3.5, 
                         'The Night Listener': 3.0},
    'Toby Higgins':     {'Snakes on a Plane': 4.5, 'Superman Returns': 4.0, 
                         'You, Me and Dupree': 1.0}
}

def sim_distance(prefs, person1, person2):
    """
    Consumes: a dict of where the keys are people and the values are dicts 
    containing ratings of items, and two people from the dict.
    Returns :a Euclidian-distance based similarity score for person1
    and person2.
    """
    prefs_1, prefs_2 = prefs[person1], prefs[person2]
    shared_items = {item for item in prefs_1 if item in prefs_2}

    # return 0 if no items in common
    if not shared_items: return 0
    
    dist = lambda item: prefs_1[item] - prefs_2[item]
    sum_squares = sum(dist(item)**2 for item in shared_items)

    return 1/(1 + sqrt(sum_squares))

 
def sim_pearsons(prefs, person1, person2):
    """
    Consumes: a dict of where the keys are people and the values are dicts 
    containing ratings of items, and two people from the dict.
    Returns: the Pearson correlation coefficient for person1 and person2
    """
    prefs_1, prefs_2 = prefs[person1], prefs[person2]
    shared_items     = {item for item in prefs_1 if item in prefs_2}

    num_elem = len(shared_items)

    # score 0 if no items in common
    if not shared_items: return 0

    sums       = lambda d, n: sum(pow(d[item], n) for item in shared_items)
    sum_1      = sums(prefs_1, 1)
    sum_2      = sums(prefs_2, 1)
    sum_sqrs_1 = sums(prefs_1, 2)
    sum_sqrs_2 = sums(prefs_2, 2)

    # sum_1, sum_2, sum_sqrs_1, sum_sqrs_2 = (
    #     sums(prefs_i, jdx) for jdx in (1,2) for prefs_i in (prefs_1, prefs_2)
    # )

    sum_prods = sum(prefs_1[item]*prefs_2[item] for item in shared_items)

    num = sum_prods - (sum_1*sum_2 / float(num_elem))
    den = sqrt((sum_sqrs_1-sum_1**2/num_elem) * (sum_sqrs_2-sum_2**2/num_elem))

    if not den: return 0
    return num / den


def top_matches(prefs, person, n=5, similarity=sim_pearsons):
    """
    Consumes: dict of persons and preferences, a person from prefs.
    Optional params: number of results and simiarity metric.
    Returns: best matches for person from prefs.
    """
    scores = ((other, similarity(prefs, person, other))
               for other in prefs if other != person)

    return sorted(scores, reverse=True, key=lambda t: t[1])[:n]


def get_recommendations(prefs, person, similarity=sim_pearsons):
    """
    Returns: list of recommendations for person using weighted 
    average of every other user's rankings.
    """
    totals   = defaultdict(int)
    sim_sums = defaultdict(int)

    for other in {k:v for k,v in prefs.items() if k != person}:
        sim = similarity(prefs, person, other)
        if sim <= 0: continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals[item] += prefs[other][item] * sim
                sim_sums[item] += sim

    rankings = ((item,total/sim_sums[item]) for item,total in totals.items())
    return sorted(rankings, reverse=True, key=lambda t: t[1])


def transform_prefs(prefs):
    """
    Consumes: a dict whose keys are people and values are dicts 
    of item: score pairs.
    Returns: a dict whose keys are items and values are dicts of 
    people: score pairs.
    """
    result = defaultdict(dict)

    for person in prefs:
        for item in prefs[person]:
            result[item][person] = prefs[person][item]

    return dict(result)

