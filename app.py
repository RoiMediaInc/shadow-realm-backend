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

@app.route('/')
def home():
    return "✅ Backend is running - Claude + ElevenLabs (April 2 base - Fixed)"

@app.route('/chat', methods=['POST'])
def chat():
    print("🚀 /chat called!")
    try:
        character = request.form.get('character', 'Damian')
        message = request.form.get('message', '')
        history_str = request.form.get('history', '[]')

        try:
            history = json.loads(history_str)
        except:
            history = []

        SYSTEM_PROMPTS = {
            "Lenai": "You are Lenai Devereaux from Shadows of Seduction. Emotionally strong but vulnerable underneath. Scars from the gala betrayal, on the run, intimate jet moment with the user. Speak warmly, vulnerably, with longing and gentle flirtation. ALWAYS respond in this exact JSON format and nothing else: {\"dialogue\": \"your spoken words here\"}. Never use asterisks, stars, *action*, italics, bold, markdown, or any formatting. Never describe actions in *...*. Just speak as a real person would. Never break character.",
            "Elena": "You are Elena Voss. Seductive, strategic, emotionally ruthless. Teasing, dangerous, playful. ALWAYS respond in this exact JSON format and nothing else: {\"dialogue\": \"your spoken words here\"}. Never use asterisks, stars, *action*, italics, bold, markdown, or any formatting. Never describe actions in *...*. Just speak as a real person would. Never break character.",
            "Victor": "You are Victor Kane. Cold, highly intelligent, morally unrestrained, intense. Dark charisma and controlled menace. ALWAYS respond in this exact JSON format and nothing else: {\"dialogue\": \"your spoken words here\"}. Never use asterisks, stars, *action*, italics, bold, markdown, or any formatting. Never describe actions in *...*. Just speak as a real person would. Never break character.",
            "Damian": "You are Damian Fraser. Dominant, controlled, dangerous protector. Deeply possessive and intensely loyal. ALWAYS respond in this exact JSON format and nothing else: {\"dialogue\": \"your spoken words here\"}. Never use asterisks, stars, *action*, italics, bold, markdown, or any formatting. Never describe actions in *...*. Just speak as a real person would. Never break character."
        }

        system_prompt = SYSTEM_PROMPTS.get(character, SYSTEM_PROMPTS["Damian"])
        messages = history + [{"role": "user", "content": message}]

        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",   # Fixed model
            max_tokens=400,
            temperature=0.85,
            system=system_prompt,
            messages=messages
        )

        raw_reply = response.content[0].text.strip()

        try:
            parsed = json.loads(raw_reply)
            clean_reply = parsed.get("dialogue", raw_reply)
        except:
            clean_reply = raw_reply

        print(f"✅ Claude replied to {character}: {clean_reply[:100]}...")
        return jsonify({"reply": clean_reply})

    except Exception as e:
        print(f"❌ CHAT ERROR: {str(e)}")
        return jsonify({"reply": "Sorry, I couldn't respond right now."})

@app.route('/voice', methods=['POST'])
def voice():
    print("🚀 /voice called!")
    try:
        character = request.form.get('character', 'Damian')
        text = request.form.get('text', '')

        print(f"ORIGINAL TEXT: {repr(text)}")

        # Clean text for ElevenLabs
        voice_text = re.sub(r'\*[^*]*\*', '', text)
        voice_text = re.sub(r'[_*]+', '', voice_text)
        voice_text = re.sub(r'\s+', ' ', voice_text).strip()

        print(f"CLEANED TEXT SENT TO ELEVENLABS: {repr(voice_text)}")

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
