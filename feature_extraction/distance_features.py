#!/usr/bin/env python3

# Total distance traveled
# Euclidean distance between start and end position
# Longest straight (highway trips)
# Shortest straight
# Long distance/short distance trip (boolean)

import numpy as np
import scipy as sp
from scipy.spatial import distance
# from scipy import stats as stats
# import math
# from sklearn.decomposition import PCA
# from sklearn.cluster import KMeans
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

samples_path = "sample_data/{}/{}.csv"

def dist_features(data):
    data_dt = [np.diff(d, axis=0) for d in data]
    dists = [np.linalg.norm(d, axis=1) for d in data_dt]
    start_end_dists = [distance.euclidean(d[0], d[-1]) for d in data]
    total_dists = [np.sum(d) for d in dists]
    median_total = np.median(total_dists)
    long_trip = [1 if d > median_total else 0 for d in total_dists]
    return [total_dists, start_end_dists, long_trip]

def straights_features(coords, dists, threshold=0.02, plot=False):
    """Create features about straights, e.g. longest, shortest, max speed, min speed
    Args:
        coords: the coordinates of the points.
        dists: the distances between the points in a trip.
        threshold: the maximum the route can deviate from being straight as a percentage. Defaults to 0.02.
    Returns:
        (longest straight, shortest straight, max speed on straight, min speed on straight)
    """
    min_straight_length = 1000
    calc_dist_diff = lambda start, end, dist_sum: dist_sum - distance.euclidean(start, end)
    diff_below_threshold = lambda dist_diff, dist_sum: abs(dist_diff) < threshold * dist_sum
    straights = identify_straights(coords, dists, threshold)
    return straights

def identify_straights(coords, dists, threshold):
    """Determine the straights from the data
    Args:
        coords: the coordinates of the points.
        dists: the distances between the points in a trip.
        threshold: the maximum the route can deviate from being straight as a percentage.
    Returns:
        list of tuples containing the starts and ends of straights.
    """
    min_straight_length = 1000
    calc_dist_diff = lambda start, end, dist_sum: dist_sum - distance.euclidean(start, end)
    diff_below_threshold = lambda dist_diff, dist_sum: abs(dist_diff) < threshold * dist_sum
    straights = {}
    end = 0
    for i in range(len(dists)):
        if i < end:
            continue
        dist_sum = dists[i]
        for j in range(i+1,len(dists)):
            dist_sum += dists[j]
            dist_diff = calc_dist_diff(coords[i], coords[j+1], dist_sum)
            if dist_sum > min_straight_length and diff_below_threshold(dist_diff, dist_sum):
                straights[i] = j+1
                end = j
    return list(straights.items())


def read_data(driver):
    return np.array([np.genfromtxt(samples_path.format(driver, trip), skip_header=1, delimiter=",") for trip in range(1, 201)])

if __name__ == '__main__':
    driver_data = [read_data(driver) for driver in range(100, 101)]
    data = driver_data[0]
    coords = data[0]
    data_dt = [np.diff(d, axis=0) for d in data]
    dists = [np.linalg.norm(d, axis=1) for d in data_dt][0]
    s = straights_features(coords, dists, 0.02, True)
    print(s)
    # features = [dist_features(d) for d in driver_data]