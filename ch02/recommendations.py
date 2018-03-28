# -*- coding: utf-8 -*-
from math import sqrt

critics = {
    'Lisa Rose':{'Lady in the Water':2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns':3.5, 'You, Me and Dupree':2.5, 'The Night Listener':3.0},
    'Gene Seymour':{'Lady in the Water':3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns':5.0, 'You, Me and Dupree':3.5, 'The Night Listener':3.0},
    'Michael Phillips':{'Lady in the Water':2.5, 'Snakes on a Plane': 3.0, 'Superman Returns':3.5, 'The Night Listener':4.0},
    'Claudia puig': {'Snakes on a Plane':3.5, 'Just My Luck':3.0, 'Superman Returns':4.0, 'You, Me and Dupree':2.0},
    'Mick LaSalle':{'Lady in the Water':3.0, 'Snakes on a Plane':4.0,'Just My Luck':2.0,'Superman Returns':3.0,'The Night Listener':3.0,'You,Me and Dupree':2.0},
    'Jack Matthews':{'Lady in the Water':3.0, 'Snakes on a Plane':4.0, 'The Night Listener':3.0, 'Superman Returns':5.0,  'You, Me and Dupree':3.5},
    'Toby':{'Snakes on a Plane':4.5, 'You, Me and Dupree':1.0, 'Superman Returns':4.0}
}

def sim_distance(prefs, person1, person2):
    si=[]
    for item in prefs[person1]:
        if item in prefs[person2]:
            si.append(item)

    if len(si) == 0: return 0

    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item],2) for item in si])
    return 1/(1+sqrt(sum_of_squares))

def sim_pearson(prefs, person1, person2):

    si=[]
    for item in prefs[person1]:
        if item in prefs[person2]:
            si.append(item)

    n = len(si)
    if n == 0: return 0

    sum1 = sum([prefs[person1][item] for item in si])
    sum2 = sum([prefs[person2][item] for item in si])

    sum1Sq = sum([pow(prefs[person1][item],2) for item in si])
    sum2Sq = sum([pow(prefs[person2][item],2) for item in si])

    pSum = sum([prefs[person1][item] * prefs[person2][item] for item in si])

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1,2)/n)*(sum2Sq - pow(sum2,2)/n))
    if den == 0: return 0

    r = num/den

    return r

def topMatches(prefs, person, n=5,similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


def get_recommendations(prefs, person, similarity=sim_pearson):
    totals={}
    sim_sum={}

    for other in prefs:
        if other == person: continue # skip my self
        sim = similarity(prefs, person, other)
        if sim < 0: continue

        for item in prefs[other]:
            if item not in prefs[person]:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim

                sim_sum.setdefault(item, 0)
                sim_sum[item] += sim

    rankings = [(total/sim_sum[item],item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

def transform_prefs(prefs):
    result = {}

    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person] = prefs[person][item]

    return result

if __name__ == '__main__':
    print(sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))
    print(sim_pearson(critics, 'Lisa Rose', 'Gene Seymour'))

    print(topMatches(critics, 'Toby', n=2))
    print(get_recommendations(critics, 'Toby'))
    print(get_recommendations(critics, 'Toby', similarity=sim_distance))

    movies = transform_prefs(critics)
    print('-' * 40)
    print(movies)
    print('-'*40)
    print(topMatches(movies, 'Superman Returns', n=1))
    #print(get_recommendations(movies, 'The Night Listener'))