import numpy as np
from corner_features import corners_features
from acceleration_features import compute_velocity, compute_scalar, acceleration_features
from read_data import read_trips
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA
import sys
from multiprocessing import Pool
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

def feature_vector(trip):
    velocity = compute_velocity(trip)
    speed = compute_scalar(velocity)
    corner_features = corners_features(velocity)
    acc_features = acceleration_features(speed)
    return np.hstack((corner_features, acc_features))

def feature_matrix(trips, feature_vector=feature_vector):
    p = Pool(3)
    return np.array(p.map(feature_vector, trips))

def feature_matrix2(trips, n=None):
    velocities = [compute_velocity(trip) for trip in trips]
    speeds = [compute_scalar(velocity) for velocity in velocities]
    maxlen = len(max(speeds, key=len)) if n is None else n
    print("maxlen:", maxlen)
    res = np.array([np.fft.fft(s, n=maxlen) for s in speeds])
    print(res.shape)
    return res


def main():
    location = "/home/joe/drivers/"
    k = int(sys.argv[1])
    trips = read_trips(location+"1")
    fmatrix = feature_matrix(trips)
    n_rows, n_comps = fmatrix.shape
    train_fmatrix = fmatrix[:int(len(fmatrix)/2)]
    train_targets = np.ones(len(train_fmatrix))
    test_fmatrix = fmatrix[int(len(fmatrix)/2):]
    test_targets = np.ones(len(test_fmatrix))
    targets = np.ones(len(fmatrix))
    for i in range(k, k+1):
        try:
            trips = read_trips(location + str(i))
            fm = feature_matrix(trips)
            print(fm.shape, fmatrix.shape, n_comps)
            train_fm = fm[:int(len(fmatrix)/2)]
            test_fm = fm[int(len(fmatrix)/2):]
            train_fmatrix = np.vstack((train_fmatrix, train_fm))
            test_fmatrix = np.vstack((test_fmatrix, test_fm))
            fmatrix = np.vstack((fmatrix, fm))

            targets = np.hstack((targets, np.zeros(len(fm)) * i))
            train_targets = np.hstack((train_targets, np.zeros(len(train_fm)) * i))
            test_targets = np.hstack((test_targets, np.zeros(len(test_fm)) * i))
            print(i)
        except IOError:
            print("error tengaleng")
    rf = RandomForestClassifier()
    rf.fit(train_fmatrix, train_targets)
    pipeline = Pipeline([('scale', StandardScaler()), ('ICA', FastICA(n_components=3))])
    transformed = pipeline.fit_transform(fmatrix)
    print(transformed.shape, targets.shape)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(transformed[:,0], transformed[:,1], transformed[:,2], c=targets, cmap=matplotlib.cm.binary)
    plt.show()

    score = rf.score(test_fmatrix, test_targets)
    print(score)

if __name__ == "__main__":
    main()
