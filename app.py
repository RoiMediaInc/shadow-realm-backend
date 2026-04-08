from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/signup', methods=['POST'])
def signup():
    print("🚀 SIGNUP FORM RECEIVED!")
    try:
        data = request.form.to_dict() if request.form else request.get_json(force=True)
        tier = data.get('tier', 'unknown')
        name = data.get('name', 'Unknown')
        email = data.get('email', 'no-email')
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        print(f"✅ RECEIVED → {timestamp} | Name: {name} | Email: {email} | Tier: {tier}")

        return jsonify({"status": "success", "message": "Data received"}), 200
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return jsonify({"status": "error"}), 500

@app.route('/', methods=['GET'])
def home():
    return "Backend is running ✅"

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
