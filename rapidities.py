import random
random.seed(12345)

import ROOT as R

fname = "tev_ll_rap_mu1m_nlow2lo.dat"

def load(fname):
    lines = open(fname)

    binning = (30,-3.1,3.1, 30,-3.1,3.1)
    h = R.TH2F("","", *binning)
    
    for line in lines:
        if line.startswith("*"):
            continue

        else:
            yp, ym, w = [float(i) for i in line.strip().split()]
            bin = h.FindBin(ym, yp)

            h.SetBinContent(bin, w)

    return h

h2d = load(fname)
s = h2d.Integral()
h2d.Scale(1./s)

hh = h2d.Clone()
hh.Reset()
for n in xrange(100000):
    hh.Fill(random.gauss(0, 2), random.gauss(0, 2))

hh.Scale(1./hh.Integral())
#h2d.Divide(hh)

yp = R.Double()
ym = R.Double()

forward = {"lplus": 0., "lminus": 0., "ll": 0.}
backward = {"lplus": 0., "lminus": 0., "ll": 0.}

for n in xrange(1000000):
    h2d.GetRandom2(yp, ym)
    deltaY = yp - ym

    if yp > 0:
        forward['lplus'] += 1
    else:
        backward['lplus'] += 1

    if ym > 0:
        forward['lminus'] += 1
    else:
        backward['lminus'] += 1

    if deltaY > 0:
        forward["ll"] += 1
    else:
        backward["ll"] += 1

print "A^ll", (forward['ll'] - backward['ll'])/float(forward['ll'] + backward['ll'])

print "A^l+", (forward['lplus'] - backward['lplus'])/float(forward['lplus'] + backward['lplus'])

print "A^l-", (forward['lminus'] - backward['lminus'])/float(forward['lminus'] + backward['lminus'])

print "A^l", (forward['lplus'] - forward['lminus'])/float(forward['lplus'] + forward['lminus'])

