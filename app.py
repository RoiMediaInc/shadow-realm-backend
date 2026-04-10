from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ Backend is running on Render"

@app.route('/chat', methods=['POST'])
def chat():
    print("🚀 /chat called!")
    try:
        data = request.form.to_dict() if request.form else request.get_json(silent=True)
        character = data.get('character', 'Lenai') if data else 'Lenai'
        message = data.get('message', '') if data else ''

        if not message:
            return jsonify({"reply": "Please type a message."})

        reply = f"Hello! You said: '{message}'. Backend is working (test mode)."

        print(f"✅ Reply sent to {character}")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return jsonify({"reply": "Sorry, I couldn't respond right now."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
