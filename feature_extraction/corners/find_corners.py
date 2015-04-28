import numpy as np
import scipy as sp
from read_data import read_trips
import matplotlib.pyplot as plt
import matplotlib
import random
import sys

def angle_between(v1, v2):
    cos_sim = np.dot(v1, v2)/(np.linalg.norm(v1) * np.linalg.norm(v2))
    return np.arccos(cos_sim)

def grad2d(arr):
    return np.vstack((np.gradient(arr[:,0]), np.gradient(arr[:,1]))).T

def smooth_low(arr):
    arr = np.array(arr, copy=True)
    for i, a in enumerate(arr):
        if np.dot(a, a) < 1:
            arr[i] = np.array([0, 0])
    return arr

def smooth(arr, n=75):
    xs = arr[:,0]
    ys = arr[:,1]
    xdft = np.fft.rfft(xs)
    ydft = np.fft.rfft(ys)
    xdft[n:] = [0]
    ydft[n:] = [0]
    xsm = np.fft.irfft(xdft)
    ysm = np.fft.irfft(ydft)
    return np.vstack((xsm, ysm)).T

def find_corners(velocity, dist=None):
    """
    Calculates where the corners are from a sequence of velocities
    Arguments:
        velocity: a sequence of 2D velocity vectors
        dist: (Optional) a sequence of scalar distances if this has already been calculated. 
    Returns:
        sequences of indices in a list. Each sequence corresponds to a corner where the indices are positions from the original trip array
    """
    if dist is None:
        v_complex = velocity[:,0] + velocity[:,1]*1j 
        dist = np.absolute(v_complex)
    res = []
    i = 0
    while i < len(velocity):
        minires = [i]
        start_vec = velocity[i]
        prev_corner_angle = 0
        currdist = dist[i]
        if dist[i] < 2:
            #if the distance from last is small it's probably noise
            i+=1
            continue
        for j, (v, d) in enumerate(zip(velocity[i+1:], dist[i+1:])):
            if d < 2:
                #if the distance from last is small it's probably noise
                v = velocity[i+j-1]
            minires.append(i+j)
            currdist += d
            corner_angle = angle_between(start_vec, v)
            if currdist > 80 or corner_angle < prev_corner_angle + np.radians(1):
                if corner_angle > np.radians(45):
                    i = i + j
                    res.append(minires)
                    break
                else:
                    break
            prev_corner_angle = corner_angle
        i += 1
    return res

def main():
    trips = read_trips(sys.argv[1])
    t_complex = [t[:,0] + t[:,1]*1j for t in trips]
    jag_velocities = [grad2d(trip) for trip in trips]
    velocities = [smooth_low(smooth(v)) for v in jag_velocities]
    v_complex = [v[:,0] + v[:,1]*1j for v in velocities]
    speeds = [np.absolute(v) for v in v_complex]
    n = random.randint(0, 199)
    n = 29
    print("Trip number is:",n)
    corners = find_corners(velocities[n])
    trip = trips[n]
    plt.scatter(trips[n][:,0], trips[n][:,1])#, c=speeds[n])
    for corner in corners:
        t = trip[corner]
        plt.plot(t[:,0], t[:,1], 'r', linewidth=4.0)
    plt.axis('equal')
    plt.show()




if __name__ == '__main__':
    main()
