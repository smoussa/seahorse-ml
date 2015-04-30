#!/usr/bin/env python3

# Total distance traveled
# Euclidean distance between start and end position
# Longest straight (highway trips)
# Shortest straight
# Long distance/short distance trip (boolean)

import datetime
import csv
# from concurrent.futures import ThreadPoolExecutor

import numpy as np
import scipy as sp
from scipy.spatial.distance import euclidean as euclid
# from scipy import stats as stats
# import math
# from sklearn.decomposition import PCA
# from sklearn.cluster import KMeans
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

samples_path = "sample_data/{}/{}.csv"
# samples_path = "../sample_data/{}/{}.csv"
features_header = ['total_dist', 'euclid_dist', 'long_trip', 'longest_strt', 'shortest_strt',
    'max_strt_spd', 'min_strt_spd']

def dist_features(data):
    data_dt = [np.diff(d, axis=0) for d in data]
    dists = [np.linalg.norm(d, axis=1) for d in data_dt]
    start_end_dists = [euclid(d[0], d[-1]) for d in data]
    total_dists = [np.sum(d) for d in dists]
    median_total = np.median(total_dists)
    long_trip = [1 if d > median_total else 0 for d in total_dists]
    straights = [straights_features(data[i], dists[i], plot=True) for i in range(len(data))]
    # with ThreadPoolExecutor(max_workers=3) as e:
    #     straights = list(e.map(lambda i:straights_features(data[i], dists[i]), range(len(data))))
    # straights = list(map(lambda i:straights_features(data[i], dists[i]), range(len(data))))
    return format(total_dists, start_end_dists, long_trip, straights)

def format(t, se, l, ss):
    """total dists, start_end_dists, long_trips, straight features"""
    return [(t[i], se[i], l[i], ss[i][0], ss[i][1], ss[i][2], ss[i][3]) for i in range(len(t))]

def straights_features(coords, dists, threshold=0.003, plot=False):
    """Create features about straights, e.g. longest, shortest, max speed, min speed
    Args:
        coords: the coordinates of the points.
        dists: the distances between the points in a trip.
        threshold: the maximum the route can deviate from being straight as a percentage.
            Defaults to 0.02.
    Returns:
        (longest straight, shortest straight, max speed on straight, min speed on
            straight)
    """
    straights = []
    while not straights:
        straights = identify_straights(coords, dists, threshold)
        threshold += 0.001
        print('No straights, new threshold: ' + str(threshold))
    features = generate_straight_features(straights)
    if plot:
        plot_straight(coords, straights)
    return features

def plot_straight(coords, straights):
    plt.figure()
    plt.plot(coords[:,0], coords[:,1])
    for s in straights:
        plt.plot(coords[s[0]:s[1],0], coords[s[0]:s[1],1], 'r')
    plt.savefig(str(datetime.datetime.now())+".svg")

def generate_straight_features(straights):
    Inf = float("inf")
    longest, shortest, fastest, slowest = 0, Inf, 0, Inf
    for s in straights:
        longest = max(longest, s[2])
        shortest = min(longest, s[2])
        fastest = max(fastest, s[2]/(s[1]-s[2]))
        slowest = min(slowest, s[2]/(s[1]-s[2]))
    return (longest, shortest, fastest, slowest)

def identify_straights(coords, dists, threshold):
    """Determine the straights from the data
    Args:
        coords: the coordinates of the points.
        dists: the distances between the points in a trip.
        threshold: the maximum the route can deviate from being straight as a percentage.
    Returns:
        list of tuples containing the starts and ends of straights.
    """
    # min dist is 10% of total length
    min_straight = 50
    calc_dist_diff = lambda start, end, dist_sum: dist_sum - euclid(start, end)
    diff_below_threshold = lambda dist_diff, dist_sum: abs(dist_diff) < threshold * dist_sum
    straights = {}
    end = 0
    for i in range(len(dists)):
        if i <= end:
            continue
        dist_sum = dists[i]
        for j in range(i+1,len(dists)):
            dist_sum += dists[j]
            dist_diff = calc_dist_diff(coords[i], coords[j+1], dist_sum)
            if dist_sum > min_straight and diff_below_threshold(dist_diff, dist_sum):
                straights[i] = (j+1, dist_sum)
                end = j
    return [(s, straights[s][0], straights[s][1]) for s in straights]


def read_data(driver):
    return np.array([np.genfromtxt(samples_path.format(driver, trip), skip_header=1, delimiter=",") for trip in range(1, 201)])

def create_csv():
    drivers = list(range(100, 101))
    driver_data = [read_data(driver) for driver in drivers]
    # for trip in range(0, 200):
    #     data = driver_data[0]
    #     coords = data[trip]
    #     data_dt = [np.diff(d, axis=0) for d in data]
    #     dists = [np.linalg.norm(d, axis=1) for d in data_dt][trip]
    #     s = straights_features(coords, dists, 0.02)
    #     print(s)
    features = [dist_features(d[:10]) for d in driver_data]
    # for driver, f in zip(drivers, features):
    #     with open('distance'+str(driver)+'.csv', 'w') as csvfile:
    #         writer = csv.writer(csvfile)
    #         writer.writerow(features_header)
    #         writer.writerows(f)

if __name__ == '__main__':
    create_csv()