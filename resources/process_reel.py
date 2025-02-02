# backend/app.py
import sys
import librosa
import numpy as np
import joblib
import os
from moviepy import VideoFileClip
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS
CORS(app)

# Load the SVM model and scaler
MODEL_PATH = "resources/svm_model.pkl"
SCALER_PATH = "resources/scaler.pkl"

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

@app.route('/process-url', methods=['POST'])
def process_url():
    data = request.json
    url = data.get('url')
    file_name = data.get('file_name')

    print(url)
    print(file_name)
    
    if not url or not file_name:
        return jsonify({"error": "Missing URL or file name"}), 400

    # Download mp4 file using yt-dlp
    commandText = f"python -m yt_dlp -o public/uploads/{file_name} {url}"
    print(commandText)
    os.system(commandText)

    file_path = f"public/uploads/{file_name}"
    if not os.path.exists(file_path):
        return jsonify({"error": "File not downloaded"}), 500

    # Extract audio from MP4 and save as WAV
    wav_path = file_path.replace('.mp4', '.wav')
    extract_audio_from_mp4(file_path, wav_path)

    # Extract features from the WAV file
    features = extract_features(wav_path)

    # Scale features and make prediction
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)

    # Return the result as JSON
    print(prediction[0])
    return jsonify({"result": prediction[0]})

if __name__ == "__main__":
    app.run(debug=True)