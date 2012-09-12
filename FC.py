import math
import operator

import scipy


class FC(object):
    def __init__(self, mubest, pdf):
        self.mubest = mubest
        self.pdf = pdf

    def R(self, x, mu):
        # P(x|mu)/P(x|mu_best)
        if self.pdf(x, mu) > 0:
            return self.pdf(x, mu)/self.pdf(x, self.mubest(x))

        else:
            return 0.
        
    def acceptance_region(self, alpha, mu, observables):
        observations = []
        for obs in observables:
            observations.append((obs,
                                 self.pdf(obs, mu),
                                 self.R(obs, mu)))

        observations.sort(key=operator.itemgetter(2),
                          reverse=True)

        # A hacky way of getting "probabilities" from our pdf
        total = sum([p for o,p,r in observations])
        
        acceptance = []
        cl = 0.
        for o, p, r in observations:
            acceptance.append(o)
            cl += p/total
            if cl >= alpha:
                break

        if cl < alpha:
            raise RuntimeError("Undercoverage, requested %.3f only got %.3f"%(alpha, cl))
            
        return acceptance

    
def normal(x, mu, sigma):
    sig2 = math.pow(sigma, 2)
    numerator = math.pow(x-mu, 2)
    return (1./math.sqrt(math.pi*2*sig2)) * math.exp(-1.*(numerator/(2*sig2)))

def normal_prob(x, mu, sigma, step=0.001):
    a = normal(x-step, mu, sigma)
    b = normal(x+step, mu, sigma)
    return step * (a+b)/2.

def poisson(observed, mean, background):
    a = math.pow(mean+background, observed)
    b = math.exp(- (mean+background))
    return a*b/math.factorial(observed)

def spin_mubest(x):
    if x < -1:
        return -1
    elif x > +1:
        return +1
    else:
        return x
    
def poisson_mubest(x):
    return max(0., x)

xxx="""
# Poisson example from FC paper
background = 3.
pois = FC(lambda x: poisson_mubest(x-background),
          lambda obs, mean: poisson(obs, mean, background))

for mu in (0.5,):# 1., 1.5, 4.5):
    belt = pois.acceptance_region(0.9, mu, range(20))
    print "%.1f: [%i, %i]"%(mu, min(belt), max(belt))

print
"""

#xxx="""
print "Bounded mean"
# Bounded mean from FC paper
mean = FC(lambda x: max(0., x),
          lambda x,mu: normal(x, mu, 1.))
for mu in (0.2, 0.4, 0.75, 1., 2.):
    belt = mean.acceptance_region(0.9, mu, scipy.linspace(-2., 4., 1000))
    print "%.3f: [%.3f, %.3f]"%(mu, min(belt), max(belt))

    #belt = mean.acceptance_region(0.9, mu, scipy.linspace(-4., 4., 1000))
    #print "%.3f: [%.3f, %.3f]"%(mu, min(belt), max(belt))

    #belt = mean.acceptance_region(0.9, mu, scipy.linspace(-6., 6., 10000))
    #print "%.3f: [%.3f, %.3f]"%(mu, min(belt), max(belt))

    belt = mean.acceptance_region(0.9, mu, scipy.linspace(-30., 30., 10000))
    print "%.3f: [%.3f, %.3f]"%(mu, min(belt), max(belt))

    #belt = mean.acceptance_region(0.9, mu, scipy.linspace(-60., 60., 100000))
    #print "%.3f: [%.3f, %.3f]"%(mu, min(belt), max(belt))
    print

xxx="""
print
print "Spin correlation FC"
# Spin correlation like
fc = FC(spin_mubest, lambda x,mu: normal(x,mu, 0.4))
for mu in (-1., -0.95, -0.9, -0.5, 0.8):
    belt = fc.acceptance_region(0.68, mu, scipy.linspace(-4., 4., 1000))
    print "mu = %+.3f: [%.3f, %.3f]"%(mu, min(belt), max(belt))
    #print "mu:", mu,
    #print max([(fc.R(x, mu), x) for x in scipy.linspace(-4., 4., 1000)])
"""
