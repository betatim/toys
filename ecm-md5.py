# This short script won me GBP200 from the
# nice people at ECM recruitment.
# http://www.ecmselection.co.uk/brainbuster/2012/10/ecm-brainbuster-nodot-34-crack-the-code-and-win-200

import time
import string
from hashlib import md5
import itertools

answer = "c6fb50c021d8f6a3cacd26542b194aa7"
phrase = "not susceptible to "


def test(guess):
    m = md5(phrase + ''.join(guess))
    
    if answer == m.hexdigest():
        return phrase + ''.join(guess)
    else:
        return False


guesses = itertools.product(*([string.letters,
                               string.lowercase,
                               string.lowercase,
                               string.lowercase,
                               string.lowercase,
                               string.lowercase + string.punctuation,
                               ]))

t = time.time()
for k in itertools.imap(test, guesses):
    if k:
        break

print time.time()-t
print k
