from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from anthropic import Anthropic

app = Flask(__name__)
CORS(app)

# Initialize Claude
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route('/')
def home():
    return "✅ Backend is running - Claude + ElevenLabs"

@app.route('/chat', methods=['POST'])
def chat():
    print("🚀 /chat called!")
    try:
        character = request.form.get('character', 'Lenai')
        message = request.form.get('message', '')

        if not message:
            return jsonify({"reply": "Please type a message."})

        # Simple system prompt
        system_prompt = f"You are {character}. Respond naturally and in character."

        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=500,
            temperature=0.8,
            system=system_prompt,
            messages=[{"role": "user", "content": message}]
        )

        reply = response.content[0].text.strip()

        print(f"✅ Claude replied: {reply[:100]}...")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ CHAT ERROR: {str(e)}")
        return jsonify({"reply": "Sorry, I couldn't respond right now."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
