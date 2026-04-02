from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from anthropic import Anthropic
import os
import re

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
    return "Backend is running - ready for /chat and /voice"

@app.route('/chat', methods=['POST'])
def chat():
    character = request.form.get('character', 'Damian')
    message = request.form.get('message', '')
    history_str = request.form.get('history', '[]')

    import json
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

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            temperature=0.85,
            system=system_prompt,
            messages=messages
        )
        raw_reply = response.content[0].text.strip()

        import json
        try:
            parsed = json.loads(raw_reply)
            clean_reply = parsed.get("dialogue", raw_reply)
        except:
            clean_reply = raw_reply

        return jsonify({"reply": clean_reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500


@app.route('/voice', methods=['POST'])
def voice():
    # Log what we receive (this is what ElevenLabs suggested)
    print(f"Content-Type: {request.content_type}")
    print(f"Form data: {dict(request.form)}")
    
    character = request.form.get('character', 'Damian')
    text = request.form.get('text', '')
    
    print(f"Character: {character}")
    print(f"ORIGINAL TEXT FROM CLAUDE: {repr(text)}")
    
    if not text:
        print("ERROR: No text provided")
        return jsonify({"error": "No text provided"}), 400

    voice_text = re.sub(r'\*[^*]*\*', '', text)
    voice_text = re.sub(r'[_*]+', '', voice_text)
    voice_text = re.sub(r'\s+', ' ', voice_text).strip()
    voice_text = voice_text.replace('asterisk', '').replace('Asterisk', '')

    print(f"FINAL CLEANED TEXT SENT TO ELEVENLABS: {repr(voice_text)}")

    if len(voice_text) > 150:
        voice_text = voice_text[:150] + "..."

    voice_id = VOICE_IDS.get(character, VOICE_IDS["Damian"])
    print(f"Using voice_id: {voice_id}")

    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json={
                "model_id": "eleven_flash_v2_5",
                "text": voice_text,
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
                "optimize_streaming_latency": 4
            },
            headers={
                "Accept": "audio/mpeg",
                "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
            }
        )
        
        print(f"ElevenLabs status code: {response.status_code}")
        if response.status_code != 200:
            print(f"ElevenLabs error response: {response.text}")
        
        response.raise_for_status()
        return Response(response.content, mimetype="audio/mpeg")
        
    except Exception as e:
        print(f"VOICE ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
