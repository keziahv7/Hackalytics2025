import streamlit as st
import soundfile as sf
import pandas as pd
import altair as alt
import numpy as np
import librosa
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import os

@st.cache_resource
def load_model():
    try:
        # Load model from JSON and weights
        with open('sentiment_model.json', 'r') as json_file:
            model_json = json_file.read()
        model = tf.keras.models.model_from_json(model_json)
        model.load_weights('Data_noiseNshift.keras')
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def extract_features(audio_data, sample_rate):
    """Extract audio features matching the model's input shape (259, 1)"""
    try:
        # Convert to mono if stereo
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Extract MFCCs
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)
        
        # Extract other features
        spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sample_rate)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sample_rate)
        zcr = librosa.feature.zero_crossing_rate(audio_data)
        
        # Combine features
        combined_features = np.concatenate([
            mfccs,
            spectral_centroids,
            spectral_rolloff,
            zcr
        ], axis=0)
        
        # Ensure we have 259 features
        if combined_features.shape[1] > 259:
            combined_features = combined_features[:, :259]
        elif combined_features.shape[1] < 259:
            pad_width = 259 - combined_features.shape[1]
            combined_features = np.pad(combined_features, ((0, 0), (0, pad_width)), mode='constant')
        
        # Reshape to match model input shape (259, 1)
        features = np.mean(combined_features, axis=0)
        features = features.reshape(259, 1)
        
        return features

    except Exception as e:
        st.error(f"Error extracting features: {str(e)}")
        return None

def preprocess_audio(audio_file):
    """Preprocess audio file for emotion detection"""
    try:
        # Read audio file
        audio_data, sample_rate = sf.read(audio_file)
        
        # Extract features
        features = extract_features(audio_data, sample_rate)
        
        if features is not None:
            # Add batch dimension
            features = np.expand_dims(features, axis=0)
            return features
        
        return None
    
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        return None

def predict_emotion(model, features):
    """Predict emotion from audio features"""
    try:
        if model is None:
            raise ValueError("Model not loaded")
        
        # Make prediction
        prediction = model.predict(features)
        
        # Get emotion labels (adjust these based on your model's classes)
        emotion_labels = ['none', 'calm', 'happy', 'sad', 'angry', 'fearful']
        
        # Get predicted emotion and confidence
        emotion_idx = np.argmax(prediction[0])
        emotion = emotion_labels[emotion_idx]
        confidence = prediction[0][emotion_idx]
        
        return {
            'emotion': emotion.capitalize(),
            'confidence': confidence,
            'raw_prediction': prediction[0]
        }
    
    except Exception as e:
        st.error(f"Error predicting emotion: {str(e)}")
        return None

def get_emotion_color(emotion):
    """Return color code for each emotion"""
    color_map = {
        'happy': '#FFD700',    # Gold
        'sad': '#87CEEB',      # Sky Blue
        'angry': '#FF6B6B',    # Red
        'fearful': '#800080',  # Purple
        'calm': '#98FB98',     # Pale Green
        'none': '#D3D3D3'      # Light Gray
    }
    return color_map.get(emotion.lower(), '#FFFFFF')

def create_chart_data(unique_emotions, raw_prediction):
    try:
        # Ensure raw_prediction has the same length as unique_emotions
        prediction_values = raw_prediction
        if len(prediction_values) != len(unique_emotions):
            # Pad or truncate prediction values to match emotions length
            prediction_values = np.pad(prediction_values, 
                (0, len(unique_emotions) - len(prediction_values)), 
                mode='constant')[:len(unique_emotions)]
        
        return pd.DataFrame({
            'Emotion': unique_emotions,
            'Probability (%)': [x * 100 for x in prediction_values]
        })
    except Exception:
        # Fallback data if there's an error
        return pd.DataFrame({
            'Emotion': unique_emotions,
            'Probability (%)': [0] * len(unique_emotions)
        })

def main():
    st.title("Audio Emotion Analysis")
    st.write("Upload an audio file to analyze the emotional content")
    
    # Sidebar with information
    with st.sidebar:
        st.header("About")
        st.write("""
        This app analyzes the emotional content of audio files.
        Supported emotions:
        - Happy
        - Sad
        - Angry
        - Fearful
        - Calm
        - None (Neutral)
        """)
        
        st.header("Instructions")
        st.write("""
        1. Upload a WAV file
        2. Wait for the analysis
        3. View the results
        """)
    
    # File uploader
    uploaded_file = st.file_uploader("Upload an audio file", type=['wav'])
    
    if uploaded_file is not None:
        # Display audio player
        st.audio(uploaded_file, format='audio/wav')
        
        # Process the audio
        with st.spinner('Processing audio...'):
            features = preprocess_audio(uploaded_file)
        
        if features is not None:
            # Load model and predict
            model = load_model()
            
            with st.spinner('Analyzing emotion...'):
                result = predict_emotion(model, features)
            
            if result:
                # Display emotion with color coding
                emotion_color = get_emotion_color(result['emotion'])
                
                # Display emotion with styled container
                st.markdown(f"""
                <div style="
                    padding: 20px;
                    border-radius: 10px;
                    background-color: {emotion_color};
                    text-align: center;
                    color: black;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 20px;
                ">
                    Detected Emotion: {result['emotion']}
                </div>
                """, unsafe_allow_html=True)
                
                # Display confidence
                st.markdown(f"### Confidence: {result['confidence']*100:.2f}%")
                
                # Create emotion probability chart
                unique_emotions = ['None', 'Calm', 'Happy', 'Sad', 'Angry', 'Fearful']
                
                # Create DataFrame for visualization using the new function
                chart_data = create_chart_data(unique_emotions, result['raw_prediction'])
                
                # Create and display bar chart
                st.markdown("### Probability Distribution")
                try:
                    chart = alt.Chart(chart_data).mark_bar().encode(
                        x='Probability (%)',
                        y=alt.Y('Emotion', sort='-x'),
                        color=alt.condition(
                            alt.datum['Probability (%)'] == max(chart_data['Probability (%)']),
                            alt.value('orange'),
                            alt.value('steelblue')
                        )
                    ).properties(height=300)
                    
                    st.altair_chart(chart, use_container_width=True)
                except Exception:
                    st.warning("Unable to display probability distribution chart")

if __name__ == "__main__":
    # Set page config
    st.set_page_config(
        page_title="Audio Emotion Analysis",
        page_icon="🎵",
        layout="wide"
    )
    
    main()
