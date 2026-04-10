from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import re
import json
import requests
from anthropic import Anthropic

app = Flask(__name__)
CORS(app)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

VOICE_IDS = {
    "Lenai": "ZUVYdNbdKEBF3OoO0Sil",
    "Elena": "MMKfmW3xC5LIBwVVKoZL",
    "Victor": "BQTfjA8kEOa1pGp1jDxb",
    "Damian": "bwFBqSVRgYJeueLra9wA"
}
print("=== REAL CLAUDE VERSION v6 - April 10 ===")
@app.route('/')
def home():
    return "✅ Backend is running - Claude + ElevenLabs (REAL CLAUDE LIVE - APRIL 10 v5)"

@app.route('/chat', methods=['POST'])
def chat():
    print("🚀 /chat called!")
    try:
        character = request.form.get('character', 'Lenai')
        message = request.form.get('message', '')

        print(f"Received from {character}: {message}")

        if not message:
            return jsonify({"reply": "Please type a message."})

        system_prompt = f"You are {character}. Respond naturally and in character."

        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=500,
            temperature=0.8,
            system=system_prompt,
            messages=[{"role": "user", "content": message}]
        )

        reply = response.content[0].text.strip()

        print(f"✅ Claude replied to {character}")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ CHAT ERROR: {str(e)}")
        return jsonify({"reply": "Sorry, I couldn't respond right now."})

@app.route('/voice', methods=['POST'])
def voice():
    print("🚀 /voice called!")
    try:
        character = request.form.get('character', 'Damian')
        text = request.form.get('text', '')

        voice_text = re.sub(r'\*[^*]*\*', '', text)
        voice_text = re.sub(r'[_*]+', '', voice_text)
        voice_text = re.sub(r'\s+', ' ', voice_text).strip()

        voice_id = VOICE_IDS.get(character, VOICE_IDS["Damian"])

        resp = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json={
                "model_id": "eleven_flash_v2_5",
                "text": voice_text,
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
            },
            headers={
                "Accept": "audio/mpeg",
                "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
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
