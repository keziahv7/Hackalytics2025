from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime
import pyrebase
from transformers import pipeline

app = Flask(__name__)

# ✅ Load Firebase Credentials
cred = credentials.Certificate(r"C:\Users\kezia\OneDrive\Attachments\MHA\Hackalytics2025\hacklytics25-679dd-firebase-adminsdk-fbsvc-a5d605a4a1.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ✅ Firebase Authentication Setup
firebase_config = {
    "apiKey": "AIzaSyBgM39U3OC5-8R-WqDYyOW__H0rM9C81sk",
    "authDomain": "hacklytics25-679dd.firebaseapp.com",
    "databaseURL": "https://hacklytics25-679dd.firebaseio.com",
    "storageBucket": "hacklytics25-679dd.appspot.com"
}
firebase = pyrebase.initialize_app(firebase_config)
firebase_auth = firebase.auth()

# ✅ Load AI Model for Sentiment Analysis
stress_analyzer = pipeline("sentiment-analysis")

@app.route("/")
def home():
    return "Flask is running!"

# ✅ AI Functions
def analyze_stress(text):
    analysis = stress_analyzer(text)
    label = analysis[0]['label']

    if label == "POSITIVE":
        return "Low"
    elif label == "NEGATIVE":
        return "High"
    return "Medium"

def suggest_coping_strategy(stress_level):
    if stress_level == "High":
        return "Try a 5-minute meditation or take deep breaths."
    elif stress_level == "Medium":
        return "Take a short walk or listen to calming music."
    return "You're doing great! Keep up the healthy routine."

# ✅ User Registration (Sign Up)
@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Create user
        user = firebase_auth.create_user_with_email_and_password(email, password)
        return jsonify({"message": "User registered successfully!", "user_id": user["localId"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ User Login
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Authenticate user
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        id_token = user["idToken"]
        return jsonify({"message": "Login successful!", "token": id_token})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Verify User Token Before Storing Entries
def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token["uid"]
    except Exception as e:
        return None

# ✅ Store Journal Entry (Only for Logged-in Users)
@app.route("/store_entry", methods=["POST"])
def store_entry():
    try:
        data = request.json
        token = data.get("token")
        text = data.get("text")

        if not token or not text:
            return jsonify({"error": "Token and text are required"}), 400

        user_id = verify_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401

        # AI Model Predicts Stress Level
        stress_level = analyze_stress(text)
        suggestion = suggest_coping_strategy(stress_level)

        # ✅ Store entry in Firestore under the user's collection
        user_collection = db.collection("users").document(user_id).collection("journal_entries")
        entry = {
            "text": text,
            "stress_level": stress_level,
            "suggestion": suggestion,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        user_collection.add(entry)

        return jsonify({"message": "Journal entry stored successfully!", "stress_level": stress_level, "suggestion": suggestion})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Retrieve Entries (Only for Logged-in Users)
@app.route("/get_entries", methods=["POST"])
def get_entries():
    try:
        data = request.json
        token = data.get("token")

        if not token:
            return jsonify({"error": "Token is required"}), 400

        user_id = verify_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401

        # Retrieve user's journal entries
        user_collection = db.collection("users").document(user_id).collection("journal_entries")
        user_entries = user_collection.stream()
        results = [{"text": entry.to_dict()["text"], "stress_level": entry.to_dict()["stress_level"], "suggestion": entry.to_dict()["suggestion"], "timestamp": entry.to_dict()["timestamp"]} for entry in user_entries]

        if not results:
            return jsonify({"message": "No journal entries found."})

        return jsonify({"entries": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Start Flask App
if __name__ == "__main__":
    app.run(debug=True)


