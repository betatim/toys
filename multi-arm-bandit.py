"""Simulation of one arm bandits with different pay out odds.

http://en.wikipedia.org/wiki/Multi-armed_bandit

Something to fiddle around with different strategies to find out which
bandit pays out the most money while trying to make as much as
possible in a limited number of rounds.
"""

import random
import operator

def bandit(p):
    def f():
        return random.random() < p
    return f


class EpsilonGreedy(object):
    def __init__(self, eps, bandits):
        self.eps = eps
        self.bandits = bandits
        # Keep track how often each of
        # the bandits has paid out
        self.stats = dict((n, [0., 0, 0]) for n,b in enumerate(bandits))

    def best(self):
        best = sorted(self.stats.iteritems(),
                      key=operator.itemgetter(1),
                      reverse=True)[0]
        return best[0]

    def winnings(self):
        w = 0
        for stat in self.stats.values():
            w += stat[1]

        return w
        
    def play(self, rounds):
        for n in xrange(rounds):
            # Take advantage of the 'best' bandit
            if random.random() > self.eps:
               best = self.best() 

            # Learn some more about the bandits
            else:
                best = random.randint(0, len(self.bandits)-1)

            payout = self.bandits[best]()
                
            if payout:
                self.stats[best][1] += 1
                self.stats[best][2] += 1

            else:
                self.stats[best][2] += 1
                
            self.stats[best][0] = (float(self.stats[best][1]) /
                                   self.stats[best][2])

        
            
payouts = [0.1]*10 + [0.4]
bandits = [bandit(f) for f in payouts]

greedy = EpsilonGreedy(0.1, bandits)
greedy.play(1000)
b = greedy.best()
print "best bandit:", b, payouts[b], greedy.winnings()

greedy = EpsilonGreedy(1., bandits)
greedy.play(1000)
b = greedy.best()
print "best bandit:", b, payouts[b], greedy.winnings()
