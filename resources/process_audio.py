import sys
import librosa
import numpy as np
import joblib
import os
from moviepy import VideoFileClip

# Load the SVM model and scaler
MODEL_PATH = "../resources/svm_model.pkl"
SCALER_PATH = "../resources/scaler.pkl"

if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    print("Error: Model or scaler file is missing.")
    sys.exit(1)

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)
        
        # Extract features
        features = {
            "chroma_stft": np.mean(librosa.feature.chroma_stft(y=y, sr=sr)),
            "rms": np.mean(librosa.feature.rms(y=y)),
            "spectral_centroid": np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
            "spectral_bandwidth": np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)),
            "rolloff": np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)),
            "zero_crossing_rate": np.mean(librosa.feature.zero_crossing_rate(y)),
        }

        # Extract MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        for i in range(20):
            features[f"mfcc{i+1}"] = np.mean(mfccs[i])

        return np.array(list(features.values())).reshape(1, -1)
    
    except Exception as e:
        print(f"Error processing audio: {e}")
        sys.exit(1)

# Function to extract audio from MP4 and save as WAV
def extract_audio_from_mp4(mp4_path, wav_path):
    try:
        # Load the video file
        video = VideoFileClip(mp4_path)

        # Extract audio
        audio = video.audio

        # Save audio as WAV
        audio.write_audiofile(wav_path, codec='pcm_s16le')

        # Close the video and audio files
        audio.close()
        video.close()

    except Exception as e:
        print(f"Error extracting audio from MP4: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_audio.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        sys.exit(1)

    # Check if the uploaded file is an MP4
    if file_path.endswith('.mp4'):
        # Extract audio from MP4 and save as WAV
        wav_path = file_path.replace('.mp4', '.wav')
        extract_audio_from_mp4(file_path, wav_path)

        # Use the extracted WAV file for feature extraction
        file_path = wav_path

    # Extract features
    features = extract_features(file_path)

    # Scale features
    features_scaled = scaler.transform(features)

    # Predict
    prediction = model.predict(features_scaled)

    # Print result
    print(prediction[0])

if __name__ == "__main__":
    main()
