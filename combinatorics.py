"""Generate all possible combinations of particles without duplicates.

This is a combinatorics engine used for particle physics. Given
several sequences of input particles we want to generate all possible
combinations of the particles in these sequences. Particles can be
composite particles, which means particles used to construct
them can not be used to for a combination.
"""


# This served as a prototype for a C++ implementation
# and so ignores lots of the features of python
class Combinations(object):
    def __init__(self, *particles):
        """Generate all combinations made of input particles

        This is not simply the product of the input sequences
        as we do not care about order (A,B) and (B,A) are just
        one combination.

        Combinations where one particle is used multiple
        times are skipped. Even if it is as part of a
        composite particle. Combining [AB, AC] and [A,B]
        will only generate [(AC, B)].
        """
        self.npools = len(particles)
        self.pools = []
        self.indices = []
        self.startpositions = []
        for i in xrange(self.npools):
            parts = particles[i]
            if i != 0:
                # check if previous list of particles
                # is the same as this one. By skipping
                # entries in this pool we avoid
                # generating duplicate combinations
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

    def dupe(self, new, excl=None):
        """Checks if `new` is already in the results excluding
        the element at position `excl` from the check
        """
        if excl is not None:
            l = self.result[:excl] + self.result[excl+1:]
        else:
            l = self.result
            
        for p in new:
            a = any(p in u for u in l)
            if a:
                return True
        return False

    def next(self):
        while True:
            dupe = False
            
            if not self.result:
                for i in xrange(self.npools):
                    pool = self.pools[i]
                    part = pool[self.startpositions[i]]
                    dupe |= self.dupe(part)
                    self.result.append(part)

            else:
                for i in reversed(xrange(self.npools)):
                    self.indices[i] += 1
                    pool = self.pools[i]
                
                    if self.indices[i] >= len(pool):
                        # Roll over
                        if self.startpositions[i] != 0:
                            # this column is special because
                            # it is the same as its immediate
                            # neighbour
                            idx = self.startpositions[i] + 1
                            self.startpositions[i] = idx
                            # this happens when we exhaust
                            # the right most pool
                            if idx == len(pool):
                                self.done = True
                                break

                        else:
                            idx = 0
                        
                        self.indices[i] = idx
                        dupe |= self.dupe(pool[idx], i)
                        self.result[i] = pool[idx]

                    else:
                        # No roll over, set new element in result
                        # and be done
                        dupe |= self.dupe(pool[self.indices[i]], i)
                        self.result[i] = pool[self.indices[i]]
                        break

                # in the C++ version detect this with i < 0
                else:
                    self.done = True
                    
            if not dupe:
                break

        if self.done:
            raise StopIteration
        else:
            return self.result


import pdb

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

# This does not do what you expect it to do
# because the duplicate lists are not
# neighbours
# XXX need an idea how to handle this case
#combos = Combinations("ABCD", 'abc', "ABCD")
#for combo in combos:
#    print combo
#print

combos = Combinations("abcd", "abcd", "abcd")
for combo in combos:
    print combo
print

combos = Combinations(["AB", "AC", "AD"], "ABCD")
for combo in combos:
    print combo
print

combos = Combinations(['AB', 'AC'], 'AB')
for combo in combos:
    print combo
print
