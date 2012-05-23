import sys
import struct
import random
random.seed = 1234

import hep_pb2


def fill_evt(event):
    for n in xrange(random.randint(0, 10)):
        j = event.jets.add()
        j.isolation = 1 * random.random()
        j = j.kin
        j.pt = 12 * random.random()
        j.eta = 2. * random.random()
        j.phi = 3.141 * random.random()
        j.E = 60 * random.random()

    for n in xrange(random.randint(0, 10)):
        j = event.electrons.add()
        j.isolation = 1 * random.random()
        j = j.kin
        j.pt = 12 * random.random()
        j.eta = 2. * random.random()
        j.phi = 3.141 * random.random()
        j.E = 60 * random.random()

    for n in xrange(random.randint(0, 10)):
        j = event.muons.add()
        j.isolation = 1 * random.random()
        j = j.kin
        j.pt = 12 * random.random()
        j.eta = 2. * random.random()
        j.phi = 3.141 * random.random()
        j.E = 60 * random.random()

collection = hep_pb2.Collection()

f = open(sys.argv[1], "wb")
for n in xrange(100000):
    #evt = collection.events.add()
    evt = hep_pb2.Event()
    evt.number = n
    fill_evt(evt)

    s = evt.SerializeToString()
    a = struct.pack("I", len(s))

    f.write(a)
    f.write(s)
    
f.close()
print "wrote events"

print "Reading events ..."
f = open(sys.argv[1], "rb")
N = 0
evt = hep_pb2.Event()

def read_until(bytes, f):
    buf = ""
    read = bytes
    while len(buf) < bytes:
        buf += f.read(read)
        if not buf:
            return None
        
        read -= len(buf)

    return buf

while True:
    msg_len = read_until(4, f)
    if msg_len is None:
        break
    
    l = struct.unpack("I", msg_len)
    
    msg = read_until(l[0], f)
    evt.ParseFromString(msg)
    N += 1

print N
