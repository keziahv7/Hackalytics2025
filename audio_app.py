import streamlit as st
import sounddevice as sd
import wavio
import os
import time
from datetime import datetime
import numpy as np
import tempfile
import speech_recognition as sr
from transformers import pipeline
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import librosa
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.io import wavfile
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

class SentimentLearner:
    def __init__(self, feedback_file='sentiment_feedback.json'):
        self.feedback_file = feedback_file
        self.feedback_data = self.load_feedback_data()
        self.model = RandomForestClassifier()
        self.label_mapping = {
            'HAPPY': 0,
            'SAD': 1,
            'ANGRY': 2,
            'FEARFUL': 3,
            'CALM': 4,
            'NEUTRAL': 5
        }
        self.retrain_model()
    
    def load_feedback_data(self):
        try:
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_feedback(self, feedback_entry):
        self.feedback_data.append(feedback_entry)
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f)
        try:
            self.retrain_model()
        except Exception:
            pass  # Silently handle retraining errors
    
    def retrain_model(self):
        if len(self.feedback_data) > 0:
            try:
                df = pd.DataFrame(self.feedback_data)
                X = df[['confidence']]
                
                # Convert string labels to numeric
                y = df['correct_sentiment'].map(self.label_mapping)
                
                # Only train if we have valid labels
                if not y.isna().all():
                    self.model.fit(X, y)
            except Exception:
                pass  # Silently handle training errors

def record_audio(duration=5):
    """Record audio for a specified duration and save to project directory"""
    try:
        # Sample rate and channels
        sample_rate = 44100
        channels = 1
        
        # Record audio
        st.write("Recording...")
        recording = sd.rec(int(duration * sample_rate),
                         samplerate=sample_rate,
                         channels=channels,
                         dtype=np.float32)
        
        # Show progress bar during recording
        progress_bar = st.progress(0)
        for i in range(duration):
            time.sleep(1)
            progress_bar.progress((i + 1) / duration)
        
        sd.wait()  # Wait until recording is finished
        
        # Normalize the audio data to be between -1 and 1
        recording = recording / np.max(np.abs(recording))
        
        # Convert to 16-bit integer format
        recording_16bit = (recording * 32767).astype(np.int16)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"voice_recording_{timestamp}.wav"
        
        # Save recording using scipy.io.wavfile
        from scipy.io import wavfile
        wavfile.write(filename, sample_rate, recording_16bit)
        
        # Create audio player section
        st.write("### Recording Playback")
        
        # Read and display the saved audio file
        with open(filename, 'rb') as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/wav')
        
        # Analyze the recording
        analysis_results = analyze_audio_sentiment(filename, st.session_state.sentiment_learner)
        
        if analysis_results:
            st.write("### Analysis Results")
            st.write(f"**Transcribed Text:** {analysis_results['text']}")
            
            sentiment = analysis_results['sentiment']
            confidence = float(analysis_results['confidence'])
            color = get_emotion_color(sentiment)
            
            st.markdown(f"""
                <div style='padding: 10px; border-radius: 5px; background-color: {color}25;'>
                    <strong>Detected Emotion:</strong> {sentiment}<br>
                    <strong>Confidence:</strong> {confidence * 100:.1f}%
                </div>
            """, unsafe_allow_html=True)
            
            # Display feedback buttons
            display_feedback_buttons(analysis_results, filename)
        
        return filename
    
    except Exception as e:
        st.error(f"Error recording audio: {str(e)}")
        return None

def load_lottieurl(url: str):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def load_lottiefile(filepath: str):
    """Load Lottie animation from local file"""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return None

def create_audio_interface():
    """Create main audio interface with tabs for recording and upload"""
    # Add custom CSS
    st.markdown(
        """
        <style>
        /* Center content */
        .center-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 1rem;
        }
        
        /* Style the button */
        .stButton > button {
            margin: 0 auto;
            display: block;
            width: 200px;
            height: 50px;
            border-radius: 25px;
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
            font-size: 16px;
            border: none;
            transition: all 0.3s ease;
        }
        
        /* Button hover effect */
        .stButton > button:hover {
            background-color: #ff3333;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4);
        }
        
        /* Button active effect */
        .stButton > button:active {
            transform: translateY(0px);
        }
        
        /* Animation container */
        .lottie-container {
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("Voice Emotion Analysis")
    
    # Create tabs for different functionalities
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Record Audio", "Upload Audio"])
    
    with tab1:
        # Create a centered container
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown('<div class="center-content">', unsafe_allow_html=True)
                
                # Animation container
                st.markdown('<div class="lottie-container">', unsafe_allow_html=True)
                lottie_recording = load_lottiefile("microphone_animation.json")  # Update path
                if lottie_recording:
                    st_lottie(
                        lottie_recording,
                        height=200,
                        key="recording_animation"
                    )
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Recording button with recording state
                if 'is_recording' not in st.session_state:
                    st.session_state.is_recording = False
                
                button_text = "⏹️ Stop Recording" if st.session_state.is_recording else "🎤 Start Recording"
                button_key = "stop_recording" if st.session_state.is_recording else "start_recording"
                
                if st.button(button_text, key=button_key):
                    st.session_state.is_recording = not st.session_state.is_recording
                    if st.session_state.is_recording:
                        # Start recording
                        recorded_file = record_audio()
                        if recorded_file:
                            st.session_state.last_recording = recorded_file
                            st.session_state.is_recording = False
                            # st.experimental_rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        handle_audio_upload_and_playback()
        

def get_emotion_color(emotion):
    """Get the appropriate color for each emotion"""
    color_map = {
        'HAPPY': '#28a745',  # Green
        'SAD': '#17a2b8',    # Blue
        'ANGRY': '#dc3545',  # Red
        'FEARFUL': '#6f42c1',# Purple
        'CALM': '#20c997',   # Teal
        'NEUTRAL': '#6c757d' # Gray
    }
    return color_map.get(emotion, '#6c757d')

def display_waveform(audio_file):
    """Display waveform visualization of the audio file"""
    try:
        # Load the audio file
        y, sr = librosa.load(audio_file)
        
        # Create figure using plotly
        import plotly.graph_objects as go
        
        # Create time axis
        time = np.linspace(0, len(y)/sr, len(y))
        
        # Create the waveform figure
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=time,
            y=y,
            mode='lines',
            name='Waveform',
            line=dict(color='#1f77b4', width=1),
        ))
        
        fig.update_layout(
            title="Audio Waveform",
            xaxis_title="Time (seconds)",
            yaxis_title="Amplitude",
            template="plotly_white",
            height=200,  # Smaller height for compact display
            margin=dict(l=0, r=0, t=30, b=0),  # Minimal margins
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error displaying waveform: {str(e)}")

def analyze_audio_sentiment(audio_file, sentiment_learner):
    """Convert audio to text and analyze sentiment with expanded emotions"""
    try:
        recognizer = sr.Recognizer()
        
        # Display waveform visualization
        st.write("### Audio Waveform")
        display_waveform(audio_file)
        
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            
            # Use a simpler sentiment analyzer
            classifier = pipeline(
                "text-classification",
                model="bhadresh-savani/distilbert-base-uncased-emotion",
                top_k=None
            )
            
            # Get emotion predictions
            results = classifier(text)
            
            # Extract all emotions and their scores
            emotions = results[0]
            
            # Create DataFrame for visualization
            emotion_data = pd.DataFrame([
                {'Emotion': emotion['label'].upper(), 'Probability': emotion['score']}
                for emotion in emotions
            ])
            
            # Sort by probability in descending order
            emotion_data = emotion_data.sort_values('Probability', ascending=False)
            
            # Display the chart
            st.write("### Emotion Probability Distribution")
            
            # Create bar chart using plotly
            fig = go.Figure(data=[
                go.Bar(
                    x=emotion_data['Emotion'],
                    y=emotion_data['Probability'],
                    marker_color=['#ff9999', '#ffd700', '#90ee90', '#87cefa', '#dda0dd', '#f0e68c', '#ffa07a']
                )
            ])
            
            fig.update_layout(
                title="Emotion Probabilities",
                xaxis_title="Emotion",
                yaxis_title="Probability",
                yaxis_range=[0, 1],
                template="plotly_white",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Map the emotion with highest score to our categories
            max_emotion = emotions[0]  # Already sorted by score
            emotion_mapping = {
                'joy': 'HAPPY',
                'sadness': 'SAD',
                'anger': 'ANGRY',
                'fear': 'FEARFUL',
                'neutral': 'NEUTRAL',
                'love': 'HAPPY',
                'surprise': 'NEUTRAL'
            }
            
            predicted_emotion = emotion_mapping.get(max_emotion['label'], 'NEUTRAL')
            
            return {
                'text': text,
                'sentiment': predicted_emotion,
                'confidence': max_emotion['score'],
                'all_emotions': {
                    emotion['label']: emotion['score'] for emotion in emotions
                }
            }
            
    except Exception as e:
        st.error(f"Error analyzing audio: {str(e)}")
        return None

def display_emotion_buttons(file_id, analysis_results):
    """Display emotion feedback buttons in a grid layout"""
    st.write("### What was the correct emotion?")
    
    # Create three rows of two buttons each
    col1, col2 = st.columns(2)
    
    # First row
    with col1:
        if st.button("😊 Happy", key=f"happy_{file_id}"):
            save_feedback(analysis_results, False, file_id, correct_emotion="HAPPY")
            st.success("Thank you for your feedback!")
            # # st.experimental_rerun()
    
    with col2:
        if st.button("😢 Sad", key=f"sad_{file_id}"):
            save_feedback(analysis_results, False, file_id, correct_emotion="SAD")
            st.success("Thank you for your feedback!")
            # # st.experimental_rerun()
    
    # Second row
    col3, col4 = st.columns(2)
    with col3:
        if st.button("😠 Angry", key=f"angry_{file_id}"):
            save_feedback(analysis_results, False, file_id, correct_emotion="ANGRY")
            st.success("Thank you for your feedback!")
            # st.experimental_rerun()
    
    with col4:
        if st.button("😨 Fearful", key=f"fearful_{file_id}"):
            save_feedback(analysis_results, False, file_id, correct_emotion="FEARFUL")
            st.success("Thank you for your feedback!")
            # st.experimental_rerun()
    
    # Third row
    col5, col6 = st.columns(2)
    with col5:
        if st.button("😌 Calm", key=f"calm_{file_id}"):
            save_feedback(analysis_results, False, file_id, correct_emotion="CALM")
            st.success("Thank you for your feedback!")
            # st.experimental_rerun()
    
    with col6:
        if st.button("😐 Neutral", key=f"neutral_{file_id}"):
            save_feedback(analysis_results, False, file_id, correct_emotion="NEUTRAL")
            st.success("Thank you for your feedback!")
            # st.experimental_rerun()

def display_feedback_buttons(analysis_results, file_id):
    """Display initial feedback buttons and handle feedback collection"""
    st.write("### Was this prediction correct?")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("👍 Correct", key=f"correct_{file_id}"):
            save_feedback(analysis_results, True, file_id)
            st.success("Thank you for your feedback!")
            # st.experimental_rerun()
            
    with col2:
        if st.button("👎 Incorrect", key=f"incorrect_{file_id}"):
            st.session_state[f'show_emotion_selection_{file_id}'] = True
            # st.experimental_rerun()
            
    with col3:
        if st.button("🤔 Unsure", key=f"unsure_{file_id}"):
            save_feedback(analysis_results, None, file_id)
            st.info("Thank you for your feedback!")
            # st.experimental_rerun()
            
    # Show emotion selection buttons if needed
    if st.session_state.get(f'show_emotion_selection_{file_id}', False):
        display_emotion_buttons(file_id, analysis_results)

def save_feedback(analysis_results, was_correct, file_id, correct_emotion=None):
    """Save feedback to improve the model"""
    feedback_entry = {
        'file_id': file_id,
        'text': analysis_results['text'],
        'predicted_sentiment': analysis_results['sentiment'],
        'confidence': analysis_results['confidence'],
        'was_correct': was_correct,
        'correct_sentiment': correct_emotion if not was_correct else analysis_results['sentiment'],
        'timestamp': datetime.now().isoformat()
    }
    
    # Add all emotion probabilities if available
    if 'all_emotions' in analysis_results:
        feedback_entry['all_emotions'] = analysis_results['all_emotions']
    
    st.session_state.sentiment_learner.save_feedback(feedback_entry)
    
    # Clear the emotion selection state if it exists
    if f'show_emotion_selection_{file_id}' in st.session_state:
        del st.session_state[f'show_emotion_selection_{file_id}']


def create_audio_player_section():
    """Create a section for audio file playback and sentiment analysis with feedback"""
    st.write("### Recording Playback and Analysis")
    
    recordings = [f for f in os.listdir('.') if f.startswith('voice_recording_')]
    recordings.sort(reverse=True)
    
    if not recordings:
        st.info("No recordings available")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_file = st.selectbox(
            "Select recording to play",
            recordings,
            key="recording_selector"
        )
        
        if selected_file:
            try:
                with open(selected_file, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/wav')
                
                # Analyze sentiment
                analysis_results = analyze_audio_sentiment(
                    selected_file, 
                    st.session_state.sentiment_learner
                )
                
                if analysis_results:
                    st.write("### Analysis Results")
                    st.write(f"**Transcribed Text:** {analysis_results['text']}")
                    
                    sentiment = analysis_results['sentiment']
                    confidence = float(analysis_results['confidence'])
                    color = get_emotion_color(sentiment)
                    
                    st.markdown(f"""
                        <div style='padding: 10px; border-radius: 5px; background-color: {color}25;'>
                            <strong>Detected Emotion:</strong> {sentiment}<br>
                            <strong>Confidence:</strong> {confidence * 100:.1f}%
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display feedback buttons
                    display_feedback_buttons(analysis_results, selected_file)
                    
            except Exception as e:
                st.error(f"Error playing file: {str(e)}")
    
    with col2:
        if selected_file:
            display_file_info(selected_file)

def display_file_info(selected_file):
    """Display file information and feedback statistics"""
    file_stats = os.stat(selected_file)
    st.write("### File Information:")
    st.write(f"Size: {file_stats.st_size / 1024:.2f} KB")
    st.write(f"Created: {datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Display feedback statistics
    if hasattr(st.session_state, 'sentiment_learner'):
        feedback_data = pd.DataFrame(st.session_state.sentiment_learner.feedback_data)
        if not feedback_data.empty:
            st.write("### Feedback Statistics:")
            total_feedback = len(feedback_data)
            correct_predictions = len(feedback_data[feedback_data['was_correct'] == True])
            accuracy = (correct_predictions / total_feedback) * 100 if total_feedback > 0 else 0
            
            st.write(f"Total Feedback: {total_feedback}")
            st.write(f"Model Accuracy: {accuracy:.1f}%")

def display_feedback_buttons(analysis_results, file_id):
    """Display initial feedback buttons and handle feedback collection"""
    st.write("### Was this prediction correct?")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("👍 Correct", key=f"correct_{file_id}"):
            save_feedback(analysis_results, True, file_id)
            st.success("Thank you for your feedback!")
            # # st.experimental_rerun()
            
    with col2:
        if st.button("👎 Incorrect", key=f"incorrect_{file_id}"):
            st.session_state.show_emotion_selection = file_id
            
    with col3:
        if st.button("🤔 Unsure", key=f"unsure_{file_id}"):
            save_feedback(analysis_results, None, file_id)
            st.info("Thank you for your feedback!")
            # # st.experimental_rerun()
            
    # Show emotion selection buttons if needed
    if hasattr(st.session_state, 'show_emotion_selection') and st.session_state.show_emotion_selection == file_id:
        display_emotion_buttons(file_id, analysis_results)

def save_feedback(analysis_results, was_correct, file_id):
    """Save feedback to improve the model"""
    feedback_entry = {
        'file_id': file_id,
        'text': analysis_results['text'],
        'predicted_sentiment': analysis_results['sentiment'],
        'confidence': analysis_results['confidence'],
        'was_correct': was_correct,
        'correct_sentiment': analysis_results.get('correct_sentiment'),
        'timestamp': datetime.now().isoformat()
    }
    
    st.session_state.sentiment_learner.save_feedback(feedback_entry)

def handle_audio_upload_and_playback():
    """Handle audio file upload and playback"""
    st.write("### Audio Upload and Analysis")
    
    uploaded_file = st.file_uploader("Upload an audio file", type=['wav'])
    
    if uploaded_file is not None:
        # Create columns for player and analysis
        col1, col2 = st.columns([2, 1])
        
        with col1:
            try:
                # Display audio player
                st.audio(uploaded_file, format='audio/wav')
                
                # Save temporary file for analysis
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    
                    # Analyze sentiment
                    analysis_results = analyze_audio_sentiment(
                        tmp_file.name, 
                        st.session_state.sentiment_learner
                    )
                    
                    if analysis_results:
                        st.write("### Analysis Results")
                        st.write(f"**Transcribed Text:** {analysis_results['text']}")
                        
                        sentiment = analysis_results['sentiment']
                        confidence = float(analysis_results['confidence'])
                        color = get_emotion_color(sentiment)
                        
                        st.markdown(f"""
                            <div style='padding: 10px; border-radius: 5px; background-color: {color}25;'>
                                <strong>Detected Emotion:</strong> {sentiment}<br>
                                <strong>Confidence:</strong> {confidence * 100:.1f}%
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Display feedback buttons
                        display_feedback_buttons(analysis_results, uploaded_file.name)
                
                os.unlink(tmp_file.name)  # Clean up temp file
                    
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
        
        with col2:
            # Display file information
            file_size = len(uploaded_file.getvalue()) / 1024  # Size in KB
            st.write("File Information:")
            st.write(f"Filename: {uploaded_file.name}")
            st.write(f"Size: {file_size:.2f} KB")
            st.write(f"Type: {uploaded_file.type}")

def main():
    """Main application entry point"""
    if 'sentiment_learner' not in st.session_state:
        st.session_state.sentiment_learner = SentimentLearner()
    
    create_audio_interface()

if __name__ == "__main__":
    # Set page config
    st.set_page_config(
        page_title="Audio Emotion Analysis",
        page_icon="🎵",
        layout="wide"
    )
    main()
