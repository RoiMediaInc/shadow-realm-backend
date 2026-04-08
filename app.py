from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import requests
from anthropic import Anthropic

app = Flask(__name__)
CORS(app)

# === SET THESE IN RENDER ENVIRONMENT VARIABLES ===
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

client = Anthropic(api_key=ANTHROPIC_API_KEY)

VOICE_IDS = {
    "Damian": "bwFBqSVRgYJeueLra9wA",
    "Lenai": "ZUVYdNbdKEBF3OoO0Sil",
    "Victor": "BQTfjA8kEOa1pGp1jDxb",
    "Elena": "MMKfmW3xC5LIBwVVKoZL"
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.form.to_dict() if request.form else request.get_json(force=True)
    character = data.get('character', 'Lenai')
    message = data.get('message', '')
    history = data.get('history', '[]')
    try:
        history = eval(history) if isinstance(history, str) else history
    except:
        history = []
    
    system_prompt = f"You are {character} from Shadows of Seduction. Respond naturally and conversationally as the character. Never use asterisks or action descriptions."
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=400,
            temperature=0.85,
            messages=messages
        )
        aiReply = response.content[0].text.strip()
        return jsonify({"reply": aiReply})
    except Exception as e:
        print("Chat error:", str(e))
        return jsonify({"reply": "Sorry, I couldn't respond right now."})

@app.route('/voice', methods=['POST'])
def voice():
    data = request.form.to_dict() if request.form else request.get_json(force=True)
    character = data.get('character', 'Damian')
    text = data.get('text', '')
    voice_id = VOICE_IDS.get(character, VOICE_IDS["Damian"])
    
    print(f"🔊 Voice request for {character} - text: {len(text)} chars")
    
    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json={
                "model_id": "eleven_flash_v2_5",
                "text": text,
                "voice_settings": {
                    "stability": 0.75,
                    "similarity_boost": 0.85
                }
            },
            headers={
                "Accept": "audio/mpeg",
                "xi-api-key": ELEVENLABS_API_KEY
            }
        )
        
        print(f"Voice response status: {response.status_code}")
        print(f"Voice response content-type: {response.headers.get('content-type')}")
        
        response.raise_for_status()
        return Response(response.content, mimetype="audio/mpeg")
        
    except Exception as e:
        print("Voice error:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Backend is running - Claude + ElevenLabs"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
