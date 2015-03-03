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

def read_data(driver, trip):
	return np.genfromtxt(samples_path.format(driver, trip), skip_header=1, delimiter=",")

driver_data = [read_data(driver, trip) for trip in range(1, 201) for driver in range(100, 101)]

features = [dist_features(d) for d in driver_data]