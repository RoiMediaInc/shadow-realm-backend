from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ Backend is running on Render"

@app.route('/chat', methods=['POST'])
def chat():
    print("🚀 /chat called!")
    try:
        character = request.form.get('character', 'Lenai')
        message = request.form.get('message', '')

        if not message:
            return jsonify({"reply": "Please type a message."})

        reply = f"Hi! You said '{message}'. Backend connection is working (test mode)."

        print(f"✅ Reply sent to {character}")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return jsonify({"reply": "Sorry, I couldn't respond right now."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
