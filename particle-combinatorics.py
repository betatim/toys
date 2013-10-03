from itertools import combinations, product
from pprint import pprint


def combos(p, Ns):
    if len(Ns) == 1:
        for comb in combinations(p, Ns[0]):
            yield ''.join(comb)

    else:
        for comb in combinations(p, Ns[0]):
            comb_ = ''.join(comb)
            for subcombo in product([comb_],list(combos(p-set(comb), Ns[1:]))):
                yield subcombo


#pprint(list(combos(set('abcd'), [2])))
#print
#pprint(list(combos(set('abcde'), [2, 2, 1])))
#print
#pprint(list(combos(set('abcd'), [2, 2])))
#print
pprint(list(combos(set('abcd'), [2, 1])))
print
#pprint(list(combos(set('abcdef'), [3])))
