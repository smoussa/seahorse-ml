from numpy import genfromtxt
import os

def read_trips(direc):
     return [genfromtxt(os.path.join(direc, str(i) +".csv"), skip_header=1, delimiter=",") for i in range(1, 201)]
