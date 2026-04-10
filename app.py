from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app)

print("✅ App starting up...")

@app.route('/')
def home():
    print("Health check received")
    return "✅ Backend is running on Render"

@app.route('/chat', methods=['POST'])
def chat():
    print("🚀 /chat called!")
    try:
        character = request.form.get('character', 'Lenai')
        message = request.form.get('message', '')

        print(f"Received from {character}: {message}")

        if not message:
            return jsonify({"reply": "Please type a message."})

        reply = f"Hi! You said '{message}'. Backend connection is working (test mode)."

        print(f"✅ Reply sent to {character}")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ CHAT ERROR: {str(e)}")
        return jsonify({"reply": "Sorry, I couldn't respond right now."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
