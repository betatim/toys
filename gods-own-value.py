import numpy as np
np.random.seed(12345)


gods_value = 42.141
trials = 10000

belts = []
for n in xrange(trials):
    x = np.random.normal(gods_value, 1.)
    # measured confidence belt
    belts.append((x-1., x+1.))

touching = 0
for low,high in belts:
    if low <= gods_value <= high:
        touching += 1

print "Our belt touches God's value: %.2f%%"%(touching/float(trials)*100)
