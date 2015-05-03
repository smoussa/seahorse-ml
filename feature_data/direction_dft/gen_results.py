import sys
import os
import csv
import numpy as np
import scipy as sp
from scipy.spatial import distance as distance
from scipy import stats as stats
import math
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from scipy.stats import chi2
import matplotlib.pyplot as plt


def find_angle(v):
    if np.linalg.norm(v) == 0:
        return 0
    xaxis = [1, 0]
    cos_sim = np.dot(xaxis, v)/np.linalg.norm(v)
    return np.arccos(cos_sim)


def no_zeros(a):
    for i, item in enumerate(a):
        if a[i] == 0:
            a[i] = a[i - 1]

def reject_outliers(data, m=2):
    thresh = m*np.std(data, axis=1)
    mean = np.mean(data, axis=1)
    return np.array([datum for datum in data.T if np.all(datum -  mean < thresh)])

def calc_confidence(trips):
    pos_diffs = [np.diff(trip, axis=0) for trip in trips]
    directions = [np.apply_along_axis(find_angle, 1, diff) for diff in pos_diffs]

    for d in directions:
        no_zeros(d)
    
    direction_diffs = [np.diff(d) for d in directions]
    max_len = max(map(len, direction_diffs))
    direction_diffs_dft = np.array([np.fft.fft(d, n=max_len) for d in direction_diffs])

    pca_red = Pipeline([('scaling', StandardScaler()), ('pca', PCA(n_components=3))]).fit_transform(direction_diffs_dft)
    no_outliers = reject_outliers(pca_red.T)
    mean_pca_red = np.mean(no_outliers.T, axis=1)
    cov_pca_red = np.cov(no_outliers.T)
    C_inv = np.linalg.inv(cov_pca_red)
    chi2_stats = [((np.matrix(t) - mean_pca_red) * C_inv * (np.matrix(t) - mean_pca_red).T).item() for t in pca_red]
    pvals = 1 - chi2.cdf(chi2_stats, df=len(chi2_stats))
    return pvals


def create_trip_list(directory):
    return [np.genfromtxt(os.path.join(directory, str(i) +".csv"), skip_header=1, delimiter=",") for i in range(1, 201)]

def directory_list(outer_dir):
    return (name for name in os.listdir(outer_dir) if os.path.isdir(os.path.join(outer_dir, name)))


def main():
    outer_dir = sys.argv[1]

    for direc in directory_list(outer_dir):
        trips = create_trip_list(os.path.join(outer_dir, direc))
        pvals = calc_confidence(trips) 
        for i, pval in enumerate(pvals):
            print("{dnum}_{tnum},{pval:.10f}".format(dnum=direc, tnum=i+1, pval=pval))


if __name__ == "__main__":
    main()
