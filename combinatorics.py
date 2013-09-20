"""Generate all possible combinations of particles without duplicates"""


# This served as a prototype for a C++ implementation
# and so ignores lots of the features of python
class Combinations(object):
    def __init__(self, *particles):
        self.npools = len(particles)
        self.pools = []
        self.indices = []
        self.startpositions = []
        for i in xrange(self.npools):
            parts = particles[i]
            if i != 0:
                # check if previous list of particles
                # is the same as this one
                if parts == particles[i-1]:
                    start = self.startpositions[i-1] + 1
                else:
                    start = 0

            else:
                start = 0

            self.startpositions.append(start)
            self.indices.append(start)
            self.pools.append(tuple(parts))
            
        self.result = []
        self.done = False

    def __iter__(self):
        return self

    def next(self):
        if not self.result:
            for i in xrange(self.npools):
                pool = self.pools[i]
                self.result.append(pool[self.startpositions[i]])

        else:
            for i in reversed(xrange(self.npools)):
                self.indices[i] += 1
                pool = self.pools[i]
                if self.indices[i] == len(pool):
                    # Roll over
                    if self.startpositions[i] != 0:
                        # this column is special because
                        # it is the same as its immediate
                        # neighbour
                        idx = self.startpositions[i] + 1
                        self.startpositions[i] = idx
                        
                    else:
                        idx = 0
                        
                    self.indices[i] = idx
                    if idx == len(pool):
                        self.done = True
                        break
                        
                    self.result[i] = pool[idx]

                else:
                    # No roll over, set new element in result
                    # and be done
                    self.result[i] = pool[self.indices[i]]
                    break

            # in the C++ version detect this by i < 0
            else:
                self.done = True

        if self.done:
            raise StopIteration
        else:
            return self.result


import pdb
#pdb.set_trace()
combos = Combinations("ABCD", "abcd")
for combo in combos:
    print combo
print

combos = Combinations("ABCD", "ABCD")
for combo in combos:
    print combo
print

combos = Combinations("ABCD", "ABCD", 'abc')
for combo in combos:
    print combo
print
