import numpy as np
from scipy.signal import find_peaks


def remove_single_width_peaks(data, peaks):
    width = 1
    filled_data = np.copy(data)
    for i in peaks:
        left = max(0, i - width)
        right = min(len(data) - 1, i + width + 1)
        filled_data[i] = np.median(filled_data[left:right])
    return filled_data.astype('int')


def remove_given_width_peaks(data, peaks, width):
    window_size = width + width // 2
    filled_data = np.copy(data)
    for i in peaks:
        peak_left = max(0, i - width)
        peak_right = min(len(data) - 1, i + width + 1)
        left = max(0, i - window_size)
        right = min(len(data) - 1, i + window_size + 1)
        filled_data[peak_left:peak_right] = np.median(filled_data[left:right])
    return filled_data.astype('int')


def get_peaks(curve, width):
    positive_peaks, _ = find_peaks(curve, width=[0, width])
    negative_peaks, _ = find_peaks(abs(curve - 1), width=[0, width])
    peaks = np.unique(np.hstack((positive_peaks, negative_peaks)))
    return peaks
