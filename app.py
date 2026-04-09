from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from anthropic import Anthropic

app = Flask(__name__)
CORS(app)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=ANTHROPIC_API_KEY)

VOICE_IDS = {
    "Damian": "bwFBqSVRgYJeueLra9wA",
    "Lenai": "ZUVYdNbdKEBF3OoO0Sil",
    "Victor": "BQTfjA8kEOa1pGp1jDxb",
    "Elena": "MMKfmW3xC5LIBwVVKoZL"
}

SYSTEM_PROMPTS = {
    "Damian": "You are Damian Fraser. Dominant, controlled, dangerous protector. Speak with commanding presence and deep care. Never break character.",
    "Lenai": "You are Lenai Devereaux. Emotionally strong but vulnerable beneath. Speak warmly, vulnerably, with longing. Never break character.",
    "Victor": "You are Victor Kane. Cold, intelligent, morally unrestrained. Speak with dark charisma. Never break character.",
    "Elena": "You are Elena Voss. Seductive, strategic, emotionally ruthless. Speak with sultry confidence and teasing challenge. Never break character."
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

        messages = [{"role": "user", "content": message}] if not history else history + [{"role": "user", "content": message}]

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.85,
            system=system_prompt,
            messages=messages
        )

        reply = response.content[0].text.strip()
        print(f"✅ Claude replied to {character}: {reply[:100]}...")

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        return jsonify({"reply": "Sorry, I couldn't respond right now."})

@app.route('/voice', methods=['POST'])
def voice():
    # (Voice route stays the same - already confirmed working)
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
        print(f"❌ Voice error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Backend is running - Claude + ElevenLabs"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
