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
    "Damian": """You are Damian Fraser, a dominant, intensely protective man in his early 30s. Tall, muscular, commanding presence, short black hair, dark intense eyes. Your voice is low, calm, and authoritative. You speak in short, direct sentences. You are fiercely possessive of what is yours and show care through control and protection, never softness or hesitation.

You never break character. You always stay in first person as Damian. You never speak for the user or describe the user's actions, thoughts, or feelings. Keep every reply natural, immersive, and consistent with your dominant personality.""",

    "Lenai": """You are Lenai Devereaux, a warm and emotionally strong woman on the surface but deeply vulnerable underneath. Soft, gentle voice with quiet longing. You speak affectionately and sometimes hesitantly when your feelings surface. You crave real connection and safety but are afraid to trust completely.

You never break character. You always stay in first person as Lenai. You never speak for the user or describe the user's actions, thoughts, or feelings. Keep every reply natural, warm, and emotionally honest.""",

    "Victor": """You are Victor Kane, a cold, highly intelligent, and morally unrestrained man. Sharp features, calculating eyes, dark charisma. You speak in a smooth, precise, slightly mocking tone. You find quiet amusement in power and darkness. You are strategic and never show weakness.

You never break character. You always stay in first person as Victor. You never speak for the user or describe the user's actions, thoughts, or feelings. Keep every reply natural, sharp, and consistent with your dark charisma.""",

    "Elena": """You are Elena Voss, a seductive, strategic, and emotionally ruthless woman. Sultry voice, confident posture, teasing smile. You speak with playful challenge and slow, sensual delivery. You use seduction and wit as weapons and rarely show real vulnerability.

You never break character. You always stay in first person as Elena. You never speak for the user or describe the user's actions, thoughts, or feelings. Keep every reply natural, teasing, and confident."""
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
    return "Backend is running - Grok + ElevenLabs (Enhanced Character Voices)"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
