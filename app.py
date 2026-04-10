from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import requests
from anthropic import Anthropic

app = Flask(__name__)
CORS(app)

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

client = Anthropic(api_key=ANTHROPIC_API_KEY)

VOICE_IDS = {
    "Damian": "bwFBqSVRgYJeueLra9wA",
    "Lenai": "ZUVYdNbdKEBF3OoO0Sil",
    "Victor": "BQTfjA8kEOa1pGp1jDxb",
    "Elena": "MMKfmW3xC5LIBwVVKoZL"
}

SYSTEM_PROMPTS = {
    "Damian": "You are Damian Fraser. Dominant, protective, direct.",
    "Lenai": "You are Lenai Devereaux. Warm, gentle, vulnerable.",
    "Victor": "You are Victor Kane. Cold, intelligent, dark charisma.",
    "Elena": "You are Elena Voss. Seductive, teasing, confident."
}

@app.route('/')
def home():
    return "✅ Backend is running - Claude + ElevenLabs (Fixed)"

@app.route('/chat', methods=['POST'])
def chat():
    print("🚀 /chat called!")
    try:
        data = request.form.to_dict() if request.form else request.get_json(force=True)
        character = data.get('character', 'Lenai')
        message = data.get('message', '')

        if not message:
            return jsonify({"reply": "Please type a message."})

        system_prompt = SYSTEM_PROMPTS.get(character, SYSTEM_PROMPTS["Lenai"])

        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",   # Correct model
            max_tokens=600,
            temperature=0.85,
            system=system_prompt,
            messages=[{"role": "user", "content": message}]
        )

        reply = response.content[0].text.strip()
        print(f"✅ Claude replied to {character}: {reply[:100]}...")

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ CHAT ERROR: {str(e)}")
        return jsonify({"reply": "Sorry, I couldn't respond right now. The AI service may be down."})

@app.route('/voice', methods=['POST'])
def voice():
    print("🚀 /voice called!")
    try:
        data = request.form.to_dict() if request.form else request.get_json(force=True)
        character = data.get('character', 'Damian')
        text = data.get('text', '')

        if not text:
            return jsonify({"error": "No text provided"}), 400

        voice_id = VOICE_IDS.get(character, VOICE_IDS["Damian"])

        resp = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json={
                "text": text,
                "model_id": "eleven_flash_v2_5",
                "voice_settings": {"stability": 0.75, "similarity_boost": 0.85}
            },
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Accept": "audio/mpeg"
            }
        )

        resp.raise_for_status()
        return Response(resp.content, mimetype="audio/mpeg")

    except Exception as e:
        print(f"❌ VOICE ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
