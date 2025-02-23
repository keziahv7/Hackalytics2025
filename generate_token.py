import firebase_admin
from firebase_admin import credentials, auth

# Load Firebase Credentials
cred = credentials.Certificate("C:\\Users\\kezia\\OneDrive\\Attachments\\MHA\\Hackalytics2025\\hacklytics25-679dd-firebase-adminsdk-fbsvc-a5d605a4a1.json")
firebase_admin.initialize_app(cred)

# Replace with your actual Firebase user UID
user_uid = "your-user-uid-here"  # You can find this in Firebase Console > Authentication > Users

# Generate a custom token for the user
custom_token = auth.create_custom_token(user_uid)

# Print the token
print("Generated Firebase Token:", custom_token.decode("utf-8"))
