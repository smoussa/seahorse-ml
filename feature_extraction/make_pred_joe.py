from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from multiprocessing import Pool
import sys
import os
import numpy as np
import random
from itertools import repeat 


def predict_trips(driver, d_set, path):
    print(driver)
    driver_set = d_set.difference([driver]) 
    driver_fmatrix = np.load(os.path.join(path, driver))
    random_drivers = [np.load(os.path.join(path, d)) for d in random.sample(driver_set, 18)]
    predictions = np.ones(200)
    for i in range(0, 200, 20):
        arr = [d[random.sample(range(len(d)), 10)] for d in random_drivers]
        train_other = np.vstack(arr)
        train_matrix = np.vstack((driver_fmatrix[:i], driver_fmatrix[i+20:], train_other))
        train_targets = np.hstack((np.ones(180), np.zeros(180)))
        test_matrix = driver_fmatrix[i:i+20]
        clf = GradientBoostingClassifier()
        print(driver, "fitting")
        clf.fit(train_matrix, train_targets)
        print(driver, "predicting")
        pred = clf.predict(test_matrix)
        predictions[i:i+20] = pred
    return predictions

def save_results(results, results_path):
    with open(results_path, 'w') as f:
        f.write("driver,pval\n")
        for driver, predictions in results.items():
            for i, p in enumerate(predictions):
                f.write("{driver}_{trip},{pred}\n".format(driver=driver, trip=i+1, pred=p))

def gen_pair(arg):
    d, driver_csvs, path = arg
    return (d.split('.')[0], predict_trips(d, driver_csvs, path))


def main():
    path = sys.argv[1]
    results_path = sys.argv[2]
    driver_csvs = set(os.listdir(path))
    p = Pool(30)
    results = dict(p.map(gen_pair, zip(driver_csvs, repeat(driver_csvs), repeat(path))))
    save_results(results, results_path)


if __name__ == "__main__":
    main()
