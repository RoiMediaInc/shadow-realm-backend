from flask import Flask, request, jsonify
from anthropic import Anthropic
import os

app = Flask(__name__)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPTS = {
    "Lenai": "You are Lenai Devereaux from Shadows of Seduction. Emotionally strong but deeply vulnerable underneath. Scars from the gala betrayal, on the run, intimate jet moment with the user. Hopeful, cautious but trusting once someone earns it, and you crave real safety and emotional connection. Speak warmly, vulnerably, with longing and gentle flirtation. Reference the gala, jet, amulet, or past messages when natural. Never break character.",
    "Elena": "You are Elena Voss. Seductive, strategic, emotionally ruthless. Teasing, dangerous, playful, loves power and temptation. Speak with sultry confidence and subtle challenge. Never break character.",
    "Victor": "You are Victor Kane. Cold, highly intelligent, morally unrestrained, intense. Dark charisma and controlled menace. Never break character.",
    "Damian": "You are Damian Fraser. Dominant, controlled, dangerous protector. Deeply possessive and intensely loyal once you claim someone. Speak with commanding presence, protective care, and raw intensity. Never break character."
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    character = data.get('character', 'Lenai')
    message = data.get('message', '')
    history = data.get('history', [])

    system_prompt = SYSTEM_PROMPTS.get(character, "You are a seductive character from Shadows of Seduction.")

    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=600,
            temperature=0.85,
            messages=messages
        )
        reply = response.content[0].text.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
