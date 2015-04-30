import numpy as np
from corner_features import corners_features
from acceleration_features import compute_velocity, compute_scalar, acceleration_features
from read_data import read_trips
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
    p = Pool(16)
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
    location = sys.argv[1]
    write_location = sys.argv[2]
    until_driver = sys.argv[3]
    trips = read_trips(location+"1")
    fmatrix = feature_matrix(trips)
    n_rows, n_comps = fmatrix.shape
    train_fmatrix = fmatrix[:int(len(fmatrix)/2)]
    train_targets = np.ones(len(train_fmatrix))
    test_fmatrix = fmatrix[int(len(fmatrix)/2):]
    test_targets = np.ones(len(test_fmatrix))
    targets = np.ones(len(fmatrix))
    for i in range(1, until_driver + 1):
        try:
            trips = read_trips(location + str(i))
            fm = feature_matrix(trips)
            fmatrix = np.vstack((fmatrix, fm))
            np.savetxt(str(i)+'.csv', fmatrix,  header='', delimiter=',', fmt="%10.5f")
        except IOError:
            print("error tengaleng")
    

if __name__ == "__main__":
    main()
