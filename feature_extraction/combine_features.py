import numpy as np
from corner_features import corners_features, angle_between, cos_between
from acceleration_features import compute_velocity, compute_scalar, acceleration_features, n_step_diff
from read_data import read_trips
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA
from  sklearn.svm import SVC
import sys
import os 
from multiprocessing import Pool

def feature_vector(trip):
    velocity = compute_velocity(trip)
    velocity5 = n_step_diff(trip, n=5)
    acceleration = np.gradient(velocity)
    acceleration5 = np.gradient(velocity5)
    cos_dt = [cos_between(a, np.array([1, 0])) for a in acceleration5]
    angle_dt = [np.arccos(c) for c in cos_dt]
    speed = compute_scalar(velocity)
    corner_features = corners_features(velocity)
    acc_features = acceleration_features(velocity, angle_dt, cos_dt, speed)
    return np.hstack((corner_features, acc_features))
    #return acc_features

def feature_matrix(trips, feature_vector=feature_vector):
    p = Pool(20)
    res = np.array(p.map(feature_vector, trips))
    p.terminate()
    return res

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
    z = sys.argv[1]
    k = int(sys.argv[2])
    trips = read_trips(location+z)
    fmatrix = feature_matrix(trips)
    n_rows, n_comps = fmatrix.shape
    train_fmatrix = fmatrix[:int(len(fmatrix)*0.9)]
    train_targets = np.ones(len(train_fmatrix))
    test_fmatrix = fmatrix[int(len(fmatrix)*0.9):]
    test_targets = np.ones(len(test_fmatrix))
    targets = np.ones(len(fmatrix))
    i = k
    j = 0
    while i < (k+20) and j < 10000:
        j +=1
        try:
            trips = read_trips(location + str(i))
            fm = feature_matrix(trips)
            train_fm = fm[:9]
            test_fm = fm[9:10]
            train_fmatrix = np.vstack((train_fmatrix, train_fm))
            test_fmatrix = np.vstack((test_fmatrix, test_fm))
            fmatrix = np.vstack((fmatrix, fm))

            targets = np.hstack((targets, np.zeros(len(fm)) * i))
            train_targets = np.hstack((train_targets, np.zeros(len(train_fm)) * i))
            test_targets = np.hstack((test_targets, np.zeros(len(test_fm)) * i))
            print(i)
            i += 1
        except IOError:
            pass

    pipeline = Pipeline([('scale', StandardScaler()), ('ICA', PCA(n_components=50))])
    pipeline.fit(fmatrix)
    train_trans = pipeline.transform(train_fmatrix)
    test_trans = pipeline.transform(test_fmatrix)

    print("point teng", num_t_targets/len(test_targets))
    gb = RandomForestClassifier(n_estimators=50)
    gb.fit(train_fmatrix, train_targets)
    gb_score = gb.score(test_fmatrix, test_targets)
    print("gb", gb_score)
    dt = DecisionTreeClassifier()
    dt.fit(train_fmatrix, train_targets)
    dt_score = dt.score(test_fmatrix, test_targets)
    print("dt", dt_score)
    svc = SVC()
    svc.fit(train_fmatrix, train_targets)
    svc_score = svc.score(test_fmatrix, test_targets)
    print("svc", svc_score)
    #rfs = [RandomForestClassifier(n_estimators=40) for i in range(20)]
    rfs = [GradientBoostingClassifier(n_estimators=100) for i in range(20)]
    scores = []
    for i, rf in enumerate(rfs):
        rf.fit(train_fmatrix, train_targets)
        scores.append(rf.score(test_fmatrix, test_targets))
        print(i, scores[i])
    print("average", np.mean(scores))

def write_files():
    pathread = sys.argv[1]
    pathwrite = sys.argv[2]
    dirs = os.listdir(pathread)
    corners_headers = ['num_corners', 'avg_corner_angle', 'max_corner_speed', 'min_corner_speed', 'avg_corner_speed']
    accn_headers1 = ['time_fast', 'time_slow', 'fraction_fast', 'fraction_slow', 'stops', 'fraction_stationary']
    accn_headers2 = ['speed'+str(i) for i in range(1, 51)]
    accn_headers3 = ['speedxangle'+str(i) for i in range(1, 51)]
    accn_headers4 = ['acc'+str(i) for i in range(1, 51)]
    accn_headers5 = ['acc2'+str(i) for i in range(1, 51)]
    accn_headers5 = ['speedxcos(angle)'+str(i) for i in range(1, 51)]
    accn_headers5 = ['accxangle'+str(i) for i in range(1, 51)]
    headers = corners_headers + accn_headers1 + accn_headers2 + accn_headers3 + accn_headers4 + accn_headers5
    header_str = ','.join(headers)
    for d in dirs:
        print("processing driver", d)
        trips = read_trips(os.path.join(pathread, d))
        fmatrix = feature_matrix(trips)
        np.save(os.path.join(pathwrite, d + '.npy'), fmatrix) 

if __name__ == "__main__":
    write_files()
    p.terminate()
