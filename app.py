from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_URL = "https://api.x.ai/v1/chat/completions"

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

@app.route('/chat', methods=['POST'])
def chat():
    print("🚀 /chat called!")
    try:
        data = request.form.to_dict() if request.form else request.get_json(force=True)
        character = data.get('character', 'Lenai')
        message = data.get('message', '')
        history = data.get('history', '[]')

        if isinstance(history, str):
            import json
            history = json.loads(history)

        system_prompt = SYSTEM_PROMPTS.get(character, SYSTEM_PROMPTS["Lenai"])

        messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]

        response = requests.post(
            GROK_URL,
            headers={"Authorization": f"Bearer {GROK_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "grok-4",
                "messages": messages,
                "temperature": 0.85,
                "max_tokens": 500
            }
        )

        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"].strip()

        print(f"✅ Grok replied to {character}: {reply[:120]}...")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ CHAT ERROR: {str(e)}")
        return jsonify({"reply": "Sorry, I couldn't respond right now."})

@app.route('/voice', methods=['POST'])
def voice():
    print("🚀 /voice called!")
    data = request.form.to_dict() if request.form else request.get_json(force=True)
    character = data.get('character', 'Damian')
    text = data.get('text', '')
    voice_id = VOICE_IDS.get(character, VOICE_IDS["Damian"])

    try:
        resp = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json={"text": text, "model_id": "eleven_flash_v2_5", "voice_settings": {"stability": 0.75, "similarity_boost": 0.85}},
            headers={"xi-api-key": os.getenv("ELEVENLABS_API_KEY"), "Accept": "audio/mpeg"}
        )
        resp.raise_for_status()
        return Response(resp.content, mimetype="audio/mpeg")
    except Exception as e:
        print(f"❌ VOICE ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Backend is running - Grok + ElevenLabs (Simplest Final Version)"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
