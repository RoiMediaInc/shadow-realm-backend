from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
CORS(app)

# ====================== GOOGLE SHEET SETUP ======================
SHEET_ID = "1HnXo9q-1MGIzvr3JV1ZWbcD7vCVBogEX8tz5ncs1vXQ"

def get_sheet():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    if not creds_json:
        print("❌ GOOGLE_CREDENTIALS environment variable not found")
        return None
    creds_dict = json.loads(creds_json)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).sheet1

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.form.to_dict() if request.form else request.get_json(force=True)
        
        tier = data.get('tier', 'free')
        name = data.get('name', 'Unknown')
        email = data.get('email', 'no-email')
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        row = [
            timestamp,
            name,
            email,
            tier,
            "New Subscriber",
            "", "", "", "1"   # Active Subscribers starts at 1
        ]

        sheet = get_sheet()
        if sheet:
            sheet.append_row(row)
            print(f"✅ ROW ADDED TO GOOGLE SHEET → {row}")
        else:
            print("❌ Could not connect to Google Sheet")

        return jsonify({"status": "success", "message": "Subscriber added"}), 200

    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Keep your existing chat and voice routes
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
