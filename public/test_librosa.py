import librosa
import sys

file_path = "/home/tyoneyam/DeepFakeDetection/public/uploads/Alex-2025_01_30-1.wav"

try:
    y, sr = librosa.load(file_path, sr=None)
    print("Audio successfully loaded")
except Exception as e:
    print(f"Error loading audio: {e}")
