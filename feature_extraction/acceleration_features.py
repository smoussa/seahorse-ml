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

def compute_velocities(position):
    jag_velocity = grad2d(position)
    velocity = smooth_low(smooth(jag_velocity))
    return velocity

def compute_accelerations(velocity):
    return grad2d(velocity)
    
def acceleration_features(speed):
    avg_speed = np.mean(speed)
    max_speed = np.max(speed)
    min_speed = np.min(speed)
    total_time = float(len(speed))

    fast_speed = 25
    slow_speed = 4
    
    fast = speed > fast_speed
    time_fast = np.sum(fast)
    slow = speed < slow_speed
    time_slow = np.sum(slow)
    
    fraction_fast = time_fast/total_time
    fraction_slow = time_slow/total_time

    stationary = speed < 0.5
    stops = np.sum(stationary)
    fraction_stationary = stops/total_time

    scalar_acc = np.gradient(speed)
    min_acc = np.min(scalar_acc * (scalar_acc > 0))
    max_acc = np.max(scalar_acc)
    avg_acc = np.mean(scalar_acc * (scalar_acc > 0))
    min_dec = np.min(np.abs(scalar_acc * (scalar_acc < 0)))
    max_dec = np.max(np.abs(scalar_acc * (scalar_acc < 0)))
    avg_dec = np.mean(np.abs(scalar_acc * (scalar_acc < 0)))
    return np.array([total_time, 
                     avg_speed, 
                     max_speed,
                     min_speed,
                     time_fast,
                     time_slow,
                     fraction_fast,
                     fraction_slow,
                     stops,
                     fraction_stationary,
                     avg_acc,
                     max_acc,
                     min_acc,
                     avg_dec,
                     max_dec,
                     min_dec])

def main():
    trips = read_trips(sys.argv[1])
    velocities = [compute_velocities(trip) for trip in trips]
    speeds = [compute_scalar(v) for v in velocities]
    features = np.array([acceleration_features(speed) for speed in speeds])
    print(features)

if __name__ == "__main__":
    main()
