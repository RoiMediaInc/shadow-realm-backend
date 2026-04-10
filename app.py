from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ Backend is running on Render - Ready"

@app.route('/chat', methods=['POST'])
def chat():
    print("🚀 /chat called!")
    try:
        data = request.form.to_dict() if request.form else request.get_json(silent=True) or {}
        character = data.get('character', 'Lenai')
        message = data.get('message', '')

        if not message:
            return jsonify({"reply": "Please type a message."})

        reply = f"Hello from the backend! You said: '{message}'. Character: {character}. (Test mode - Claude not connected yet)"

        print(f"✅ Reply sent to {character}")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return jsonify({"reply": "Sorry, I couldn't respond right now."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
