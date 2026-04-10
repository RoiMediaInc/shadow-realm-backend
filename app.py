from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ Backend is running - Claude + ElevenLabs"

@app.route('/chat', methods=['POST'])
def chat():
    print("🚀 /chat called!")
    try:
        data = request.form.to_dict() if request.form else request.get_json(force=True)
        character = data.get('character', 'Lenai')
        message = data.get('message', '')

        if not message:
            return jsonify({"reply": "Please type a message."})

        # Simple test reply
        reply = f"Hello! You said '{message}'. Backend is working."

        print(f"✅ Reply sent to {character}: {reply}")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ CHAT ERROR: {str(e)}")
        return jsonify({"reply": "Sorry, I couldn't respond right now."})

@app.route('/voice', methods=['POST'])
def voice():
    print("🚀 /voice called!")
    return jsonify({"error": "Voice not implemented yet"}), 501

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
