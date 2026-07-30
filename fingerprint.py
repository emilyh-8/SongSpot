import librosa
import numpy as np
from scipy.ndimage import maximum_filter
import hashlib

def load_audio(filepath):
    y, sr = librosa.load(filepath, sr=22050, mono=True)
    return y, sr


def compute_spectrogram(y):
    spectrogram = librosa.stft(y, n_fft = 4096, hop_length = 512)
    magnitude = np.abs(spectrogram)
    db_spectrogram = librosa.amplitude_to_db(magnitude, ref = np.max)
    return db_spectrogram


# This function finds the peaks in each 20x20 grid, and replaces the value with the maximum value found in the neighborhood. (grid of booleans)
def find_peaks(spectrogram):
    struct = np.ones((20, 20))
    local_max = maximum_filter(spectrogram, footprint=struct) == spectrogram
    threshold = np.median(spectrogram)
    

    detected_peaks = local_max & (spectrogram > threshold)

    freq_idx, time_idx = np.where(detected_peaks) #This helps find the actual (freq, time) coordinates of the detected peaks, reformatting from True values
    peaks = list(zip(freq_idx, time_idx)) # Created list of coordinates
    

    return peaks

# Creating local peak-pairs, fingerprinting
def generate_hashes(peaks, fan_value=15, max_time_delta=200):
    peaks = sorted(peaks, key=lambda p: p[1])  # sort by time
    hashes = []

    for i in range(len(peaks)):
       for j in range(1, fan_value):
           if i + j < len(peaks):
                freq1, t1 = peaks[i]
                freq2, t2 = peaks[i + j]
                t_delta = t2-t1

                if 0 <= t_delta <= max_time_delta:
                    combined = f"{freq1} | {freq2} | {t_delta}"
                    h = hashlib.sha1(combined.encode()).hexdigest()
                    hashes.append((h, int(t1)))


    return hashes

def fingerprint_file(filepath):
    y, sr = load_audio(filepath)
    spectrogram = compute_spectrogram(y)
    hashes = generate_hashes(find_peaks(spectrogram), fan_value=15, max_time_delta=200)
    return hashes


