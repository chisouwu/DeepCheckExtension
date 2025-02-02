import librosa
import numpy as np
import sys

file_path = sys.argv[1]

try:
    y, sr = librosa.load(file_path, sr=None)
    print("✅ Audio loaded successfully.")

    # Extract features step by step
    print("Extracting chroma_stft...")
    chroma_stft = np.mean(librosa.feature.chroma_stft(y=y, sr=sr))

    print("Extracting RMS...")
    rms = np.mean(librosa.feature.rms(y=y))

    print("Extracting spectral centroid...")
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))

    print("Extracting spectral bandwidth...")
    spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))

    print("Extracting rolloff...")
    rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))

    print("Extracting zero crossing rate...")
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))

    print("Extracting MFCCs...")
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_means = [np.mean(mfccs[i]) for i in range(20)]

    print("✅ Feature extraction successful.")
except Exception as e:
    print(f"❌ Error extracting features: {e}")
