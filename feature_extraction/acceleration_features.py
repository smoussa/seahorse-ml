import numpy as np
from read_data import read_trips
import sys
import scipy as sp

def smooth_low(arr):
    arr = np.array(arr, copy=True)
    for i, a in enumerate(arr):
        if np.dot(a, a) < 1:
            arr[i] = np.array([0, 0])
    return arr

def smooth(arr, n=75):
    xs = arr[:,0]
    ys = arr[:,1]
    xdft = np.fft.rfft(xs)
    ydft = np.fft.rfft(ys)
    xdft[n:] = [0]
    ydft[n:] = [0]
    xsm = np.fft.irfft(xdft)
    ysm = np.fft.irfft(ydft)
    return np.vstack((xsm, ysm)).T

def grad2d(arr):
    return np.vstack((np.gradient(arr[:,0]), np.gradient(arr[:,1]))).T

def compute_scalar(a):
    a_complex = a[:,0] + a[:,1]*1j
    return np.absolute(a_complex)

def compute_velocity(position):
    jag_velocity = grad2d(position)
    velocity = smooth_low(smooth(jag_velocity))
    return velocity

def compute_acceleration(velocity):
    return grad2d(velocity)
    
def acceleration_features(velocity, angle_dt, cos_dt, speed=None):
    if speed is None:
        speed = compute_scalar(velocity)

    avg_speed = np.mean(speed)
    max_speed = np.max(speed)
    min_speed = np.min(speed)
    total_time = float(len(speed))
    four_speed = (speed[0:4:-4] + speed[1:4:-3] + speed[2:4:-2] + speed[3:4:-1])/4

    fast_speed = 25
    slow_speed = 4
    
    fast = speed > fast_speed
    time_fast = np.sum(fast)
    slow = speed < slow_speed
    time_slow = np.sum(slow)

    speed_bins = np.hstack((np.linspace(0, 40, 20), np.inf))
    speed_hist, outside = np.histogram(speed, bins=speed_bins)
    n_speed_hist = speed_hist/total_time

    four_speed_bins = np.hstack((np.linspace(0, 40, 20), np.inf))
    four_speed_hist, outside = np.histogram(four_speed, bins=four_speed_bins)
    n_four_speed_hist = four_speed_hist/total_time
    
    fraction_fast = time_fast/total_time
    fraction_slow = time_slow/total_time

    stationary = speed < 0.5
    stops = np.sum(stationary)
    fraction_stationary = stops/total_time

    acc_bins = np.hstack((-np.inf, np.linspace(-10, 10, 20), np.inf))
    scalar_acc = np.gradient(speed)
    acc_hist, bins = np.histogram(scalar_acc, bins=acc_bins)
    n_acc_hist = acc_hist/total_time

    angle_dt_speed = speed * angle_dt
    angle_bins = np.hstack((-np.inf, np.linspace(-50, 50, 20), np.inf))
    angle_hist, b = np.histogram(angle_dt_speed, bins=angle_bins)
    n_angle_hist = angle_hist/total_time

    angle_dt_acc = scalar_acc*angle_dt
    angle_bins = np.hstack((-np.inf, np.linspace(-50, 50, 20), np.inf))
    acc_angle_hist, b = np.histogram(angle_dt_acc, bins=angle_bins)
    n_acc_angle_hist = acc_angle_hist/total_time

    cos_dt_speed = speed * cos_dt
    cos_bins = np.hstack((-np.inf, np.linspace(0, 40, 20), np.inf))
    cos_hist, b = np.histogram(cos_dt_speed, bins=cos_bins)
    n_cos_hist = cos_hist/total_time

    max_acc = np.max(scalar_acc)
    avg_acc = np.mean(scalar_acc * (scalar_acc > 0))
    max_dec = np.max(np.abs(scalar_acc * (scalar_acc < 0)))
    avg_dec = np.mean(np.abs(scalar_acc * (scalar_acc < 0)))
    feats1 = np.array([total_time, 
                     time_fast,
                     time_slow,
                     fraction_fast,
                     fraction_slow,
                     stops,
                     fraction_stationary])
    return np.hstack((feats1, n_speed_hist, n_angle_hist, n_acc_hist, n_cos_hist, n_acc_angle_hist))
    #return np.hstack((feats1, n_speed_hist, n_four_speed_hist, n_acc_hist, n_angle_hist))

def main():
    trips = read_trips(sys.argv[1])
    velocities = [compute_velocity(trip) for trip in trips]
    speeds = [compute_scalar(v) for v in velocities]
    features = np.array([acceleration_features(speed) for speed in speeds])
    print(features)

if __name__ == "__main__":
    main()
