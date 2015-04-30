import numpy as np
import scipy as sp
from read_data import read_trips
import matplotlib.pyplot as plt
import matplotlib
from acceleration_features import compute_velocity, compute_scalar
import random
import sys

def angle_between(v1, v2):
    cos_sim = np.dot(v1, v2)/(np.linalg.norm(v1) * np.linalg.norm(v2))
    return np.arccos(cos_sim)

def identify_corners(velocity, dist=None):
    """
    Calculates where the corners are from a sequence of velocities
    Arguments:
        velocity: a sequence of 2D velocity vectors
        dist: (Optional) a sequence of scalar distances if this has already been calculated. 
    Returns:
        sequences of indices in a list. Each sequence corresponds to a corner where the indices are positions from the original trip array
    """
    if dist is None:
        dist = compute_scalar(velocity)
    res = []
    angles = []
    i = 0
    while i < len(velocity) - 1:
        if angle_between(velocity[i], velocity[i+1]) > np.radians(5):
            start = i
            start_vec = velocity[i]
            prev_corner_angle = 0
            currdist = dist[i]
            if dist[i] < 1:
                #if the distance from last is small it's probably noise
                i+=1
                continue
            for j, (v, d) in enumerate(zip(velocity[i+1:], dist[i+1:])):
                if d < 1:
                    #if the distance from last is small it's probably noise
                    continue
                currdist += d
                corner_angle = angle_between(start_vec, v)
                if currdist > 70 or corner_angle <= prev_corner_angle + np.radians(1):
                    if corner_angle > np.radians(45):
                        i = i + j
                        res.append([start, i])
                        angles.append(corner_angle)
                        break
                    else:
                        break
                prev_corner_angle = corner_angle
        i += 1
    return (res, angles)

def corners_features(velocity, dists=None):
    if dists is None:
        dists = compute_scalar(velocity)
    corners, angles = identify_corners(velocity, dists)
    if len(corners) == 0:
        return np.array([0., 0., 0., 0., 0.])
    corner_speeds = [np.mean(dists[range(c1, c2+1)]) for c1, c2 in corners]
    max_speed = np.max(corner_speeds)
    min_speed = np.min(corner_speeds)
    mean_speed = np.mean(corner_speeds)
    return np.array([float(len(corners))/np.sum(dists), np.mean(angles), max_speed, min_speed, mean_speed])

def main():
    trips = read_trips(sys.argv[1])
    velocities = [compute_velocity(trip) for trip in trips]
    speeds = [compute_scalar(v) for v in velocities]
    features = np.array([corners_features(v, s) for v, s in zip(velocities, speeds)])
    print(features)
    n = random.randint(0, 199)
    print("Trip number is:", n)
    (corners, angles) = identify_corners(velocities[n])
    trip = trips[n]
    plt.scatter(trips[n][:,0], trips[n][:,1])#, c=speeds[n])
    for start, end in corners:
        t = trip[list(range(start, end+1))]
        plt.plot(t[:,0], t[:,1], 'r', linewidth=4.0)
    plt.axis('equal')
    plt.show()

if __name__ == '__main__':
    main()
