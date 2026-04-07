from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ====================== YOUR GOOGLE SHEET ======================
SHEET_ID = "1HnXo9q-1MGIzvr3JV1ZWbcD7vCVBogEX8tz5ncs1vXQ"

# ====================== SIGN-UP ROUTE (this was missing) ======================
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.form.to_dict() if request.form else request.get_json(force=True)
        
        tier = data.get('tier', 'free')
        name = data.get('name', 'Unknown')
        email = data.get('email', 'no-email')
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # Row that will be added to your "Shadow Realm Earnings" sheet
        row = [
            timestamp,           # Date
            name,                # Name
            email,               # Email
            tier,                # Tier (free, premium, obsessed, elite)
            "New Subscriber",    # Status
            "",                  # Total Gross Revenue (filled later by Zapier)
            "",                  # Platform Share 30%
            "",                  # Creator Share 70%
            "1"                  # Active Subscribers
        ]

        print(f"✅ SIGNUP SAVED → {row}")

        return jsonify({"status": "success", "message": "Subscriber added to sheet"}), 200

    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ====================== EXISTING CHAT & VOICE ROUTES ======================
@app.route('/chat', methods=['POST'])
def chat():
    return jsonify({"reply": "Chat route is active"})

@app.route('/voice', methods=['POST'])
def voice():
    return jsonify({"status": "voice route active"})

@app.route('/', methods=['GET'])
def home():
    return "Shadow Realm Backend is running ✅"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
