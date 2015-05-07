#!/usr/bin/env python3

# Total distance traveled
# Euclidean distance between start and end position
# Longest straight (highway trips)
# Shortest straight
# Long distance/short distance trip (boolean)

import datetime
import csv
import os
from multiprocessing import Pool
import functools

import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

samples_dir_path = "drivers/{0}/"
samples_path = samples_dir_path+"{1}.csv"
data_output_path = "feature_data/distances/distance{0}.csv"
features_header = ['total_dist', 'euclid_dist', 'long_trip', 'longest_strt', 'shortest_strt',
    'max_strt_spd', 'min_strt_spd']
pool_size = 40

def euclid(a, b):
    return np.linalg.norm(a-b)

def dist_features(data):
    data_dt = [np.diff(d, axis=0) for d in data]
    dists = [np.linalg.norm(d, axis=1) for d in data_dt]
    start_end_dists = [euclid(d[0], d[-1]) for d in data]
    total_dists = [np.sum(d) for d in dists]
    median_total = np.median(total_dists)
    long_trip = [1 if d > median_total else 0 for d in total_dists]
    # straights = [straights_features(data[i], dists[i], plot=True) for i in range(len(data))]
    pool = Pool(15)
    straights = list(pool.map(func, zip(data, dists)))
    pool.close()
    pool.join()
    return format(total_dists, start_end_dists, long_trip, straights)
def func(data_dist):
    return straights_features(data_dist[0], data_dist[1])

def format(t, se, l, ss):
    """total dists, start_end_dists, long_trips, straight features"""
    return [(t[i], se[i], l[i], ss[i][0], ss[i][1], ss[i][2], ss[i][3]) for i in range(len(t))]

def straights_features(coords, dists, threshold=0.01, plot=False):
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
    straights = identify_straights(coords, dists, threshold)
    # while not straights:
    #     straights = identify_straights(coords, dists, threshold)
    #     threshold += 0.01
    #     print('No straights, new threshold: ' + str(threshold))
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
    if not straights:
        return (0,0,0,0)
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
    def calc_dist_diff(start, end, dist_sum):
        return dist_sum - euclid(start, end)
    def diff_below_threshold(dist_diff, dist_sum):
        return abs(dist_diff) < threshold * dist_sum
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
    for trip in range(1, 201):
        path = samples_path.format(driver, trip)
        if os.path.exists(path):
            yield np.genfromtxt(path, skip_header=1, delimiter=",")
        else:
            print("Didn't find trip {0} for {1}".format(trip, driver))

def read_driver_data(driver):
    if os.path.exists(samples_dir_path.format(driver)):
        array = np.array(list(read_data(driver)))
        if array.shape:
            return driver, array
    else:
        print("Skipping driver {0}".format(driver))
        return None

def generate_all_features(driver):
    driver_data = read_driver_data(driver)
    if not driver_data:
        return
    i, d = driver_data
    print("Processing driver {0}".format(i))
    f = dist_features(d)
    with open(data_output_path.format(i), 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(features_header)
        writer.writerows(f)

def create_csv():
    drivers = list(range(1600, 2000))
    for d in drivers:
        generate_all_features(d)

if __name__ == '__main__':
    create_csv()
