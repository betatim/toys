#! /usr/bin/env python
"""Spotify ticket lottery

http://www.spotify.com/uk/jobs/tech/ticket-lottery/

How to go to the theatre by entering a ticket lottery. Cool thing
about this is there is the brute force 'simulation' approach which is
slow and imprecise and also the super fast and precise 'use maths'
approach.
"""

import math
import random
random.seed(12345)
#import multiprocessing


def comb(n, k):
    return math.factorial(n) / float(math.factorial(n-k) * math.factorial(k))

# Calculate the answer
def hyper_geo(N, m, n, k):
    return comb(m, k) * comb(N-m, n-k) / comb(N, n)

def prob(entrants, winners, tickets, members):
    # need at least this many winners
    min_winners = int(math.ceil(members / float(tickets)))
    P = 0.
    for n in xrange(min_winners, members+1):
        p = hyper_geo(entrants, members, winners, n)
        P += p

    return P
    
# You could also simulate it but it takes forever
def draw(pool, winners):
    """Draw `winners` number of people from the `pool`"""
    for n in xrange(winners):
        c = random.choice(pool)
        pool.remove(c)
        yield c

def pseudo_experiments(args):
    """Simulate N rounds of the lottery"""
    N, entrants, winners, tickets, members = args

    outcomes = []
    for n in xrange(N):
        pool = range(entrants)
        winners_ = draw(pool, winners)
        winning_members = len([w for w in winners_ if w < members])
        outcomes.append(winning_members * tickets >= members)

    return outcomes

# This is the brute force 'simulation' approach
#Npse = 10000000
#pool = multiprocessing.Pool()
#args = ((Npse, 100, 10, 2, 1), (Npse, 100, 10, 2, 2), (Npse, 10, 10, 5, 1))

#for res in pool.map(pseudo_experiments, args):
#    print sum(res) / float(Npse)
#print "="*70

# Hard coded examples
#print prob(100, 10, 2, 1)
#print prob(100, 10, 2, 2)
#print prob(10, 10, 5, 1)

# Read from stdin, expecting four integers as in the problem description
a = raw_input()
print prob(*[int(x) for x in a.split()])
