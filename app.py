from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# Supabase connection
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Character replies (easy to expand later)
CHARACTER_REPLIES = {
    "Damian": [
        "Tell me exactly what you need right now, little one. I won’t ask twice.",
        "You should be a little afraid of me. It makes this more interesting.",
        "I’ve been waiting for you since the night of the gala heist.",
        "Once I claim something, it’s mine. Forever."
    ],
    "Lenai": [
        "I feel safe with you… more than I’ve felt with anyone since the gala.",
        "That night on the jet… I still remember how you held me.",
        "You make me feel things I thought I’d buried after the gala.",
        "Tell me more about what you’re feeling. I want to hear everything."
    ],
    "Victor": [
        "You say that like you know me. Like we're old friends.",
        "I’m not the sweet type, darling. I like the edge.",
        "You’re playing a dangerous game with me… and I’m enjoying every second.",
        "Tell me what you’re willing to risk."
    ],
    "Elena": [
        "Mmm… you have no idea how dangerous that request is. But I like it.",
        "You’re far too tempting for your own good.",
        "Keep going. Tell me exactly how you want me to touch you.",
        "I burn hot. Ask me what I want… I won’t hold back."
    ]
}

@app.route('/signup', methods=['POST'])
def signup():
    print("🚀 /signup called!")
    try:
        data = request.form.to_dict() if request.form else request.get_json(force=True)
        tier = data.get('tier', 'free')
        name = data.get('name', 'Unknown')
        email = data.get('email', 'no-email')

        response = supabase.table("subscribers").insert({
            "name": name,
            "email": email,
            "tier": tier,
            "status": "active"
        }).execute()

        print(f"✅ SUBSCRIBER SAVED IN SUPABASE → {name} | {email} | Tier: {tier}")
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"❌ Signup error: {e}")
        return jsonify({"status": "error"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    print("🚀 /chat called!")
    try:
        data = request.form.to_dict() if request.form else request.get_json(force=True)
        character = data.get('character', 'Lenai')
        message = data.get('message', '')

        replies = CHARACTER_REPLIES.get(character, CHARACTER_REPLIES["Lenai"])
        reply = replies[0]  # You can make this more intelligent later

        print(f"Chat with {character}: {reply}")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ Chat error: {e}")
        return jsonify({"reply": "Sorry, I couldn't respond right now."})

@app.route('/voice', methods=['POST'])
def voice():
    return jsonify({"status": "voice route active"})

@app.route('/', methods=['GET'])
def home():
    return "TEST123 - Claude version is now live"

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
