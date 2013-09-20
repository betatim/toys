from pprint import pprint

# Detection asymmetry modelled
# using four regions in the velo
# and muon system. Top/bottom and
# left/right. Each have their own
# detection efficiency. For the muon
# system which is behind the magnet
# this efficiency also depends on
# the charge of the track

# Velo like, different efficiencies
# in left and right half only
# choosen to give same average
# efficiency as for VP left/right
velo = {"top left": .725,
        "bottom left": .725,
        "top right": .75, #(.77+.66)/2,#.735, #.65,
        "bottom right": .75 #(.77+.66)/2,#.735, #.65,
}
print "Velo:"
pprint(velo)
# VeloPix like, different efficiencies
# in all quadrants, one turned off!
vp = {"top left": velo["top left"] - .04,
      "top right":  velo["top right"] + .05,
      "bottom left":  velo["bottom left"] + .04,
      "bottom right": velo["bottom right"] - .05,
}
print "VP:"
pprint(vp)
# top and bottom asymmetry in the
# post magnet detector
top_bottom_asym = 0.03
muons = {"top left +1": .7,
         "top left -1": .7,
         "top right +1": .7,
         "top right -1": .7,
         "bottom left +1": .7-top_bottom_asym,
         "bottom left -1": .7-top_bottom_asym,
         "bottom right +1": .7-top_bottom_asym,
         "bottom right -1": .7-top_bottom_asym,
}
print "Spectrometer:"
pprint(muons)

# Number of +ve and -ve
# muons detected by polarity
Npos_velo = {-1: 0., +1: 0.}
Nneg_velo = {-1: 0., +1: 0.}
Npos_vp = {-1: 0., +1: 0.}
Nneg_vp = {-1: 0., +1: 0.}

# efficiency does not have to reverse
# perfectly when the polarity is flipped
# as running conditions will vary over time
reversal_asym = 0.1

#print "pol T/B L/R C e_velo e_muon"
for polarity in (-1, +1):
    for half in ("top", "bottom"):
        for side in ("left", "right"):
            e_velo = velo[half+" "+side]
            e_vp = vp[half+" "+side]
            for charge in (-1, +1):
                e_muon = muons[half+" "+side+" %+g"%(charge*polarity)]

                e_muon += charge * reversal_asym
                #print polarity, half, side, charge,
                #print e_velo, e_muon, e_velo*e_muon
                if charge > 0:
                    Npos_velo[polarity] += e_velo*e_muon
                    Npos_vp[polarity] += e_vp*e_muon
                else:
                    Nneg_velo[polarity] += e_velo*e_muon
                    Nneg_vp[polarity] += e_vp*e_muon

print
N = 10000
for k in Nneg_velo:
    Nneg_velo[k] = round(Nneg_velo[k]*N)
for k in Npos_velo:
    Npos_velo[k] = round(Npos_velo[k]*N)
for k in Nneg_vp:
    Nneg_vp[k] = round(Nneg_vp[k]*N)
for k in Npos_vp:
    Npos_vp[k] = round(Npos_vp[k]*N)

print "Muon eff reversal asymmetry: %.3f"%(reversal_asym)
print

def print_asym(Nneg_velo_, Npos_velo_, Nneg_vp_, Npos_vp_):
    velo_asym = (float(Nneg_velo_-Npos_velo_) /
                 (Nneg_velo_+Npos_velo_))
    print "Velo like: Nneg=%i Npos=%i A=%.6f"%(Nneg_velo_,
                                               Npos_velo_,
                                               velo_asym)
    vp_asym = (float(Nneg_vp_-Npos_vp_) /
               (Nneg_vp_+Npos_vp_))
    print "VP   like: Nneg=%i Npos=%i A=%.6f"%(Nneg_vp_,
                                               Npos_vp_,
                                               vp_asym)
    return velo_asym, vp_asym

print "For magnet DOWN:"
velo_down, vp_down = print_asym(Nneg_velo[-1], Npos_velo[-1],
                                Nneg_vp[-1], Npos_vp[-1],)
print
print "For magnet UP:"
velo_up, vp_up = print_asym(Nneg_velo[+1], Npos_velo[+1],
                            Nneg_vp[+1], Npos_vp[+1])
print
print "Combining polarities:"
print_asym(Nneg_velo[-1] + Nneg_velo[+1],
           Npos_velo[-1] + Npos_velo[+1],
           Nneg_vp[-1] + Nneg_vp[+1],
           Npos_vp[-1] + Npos_vp[+1])
print
print "Averaging both polarities:"
print "Velo A=%.6f"%((velo_down+velo_up)/2)
print "VP   A=%.6f"%((vp_down+vp_up)/2)
