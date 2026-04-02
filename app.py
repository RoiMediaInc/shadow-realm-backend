import re

@app.route('/voice', methods=['POST'])
def voice():
    data = request.json
    character = data.get('character', 'Damian')
    text = data.get('text', '')

    # ULTRA aggressive cleaning — removes every *action*, _action_, leftover * or _
    voice_text = re.sub(r'\*[\s\S]*?\*', '', text)   # removes anything between * and *
    voice_text = re.sub(r'[_*]+', '', voice_text)    # removes any * or _ left behind
    voice_text = re.sub(r'\s+', ' ', voice_text).strip()

    # Shorten long responses to reduce latency even more
    if len(voice_text) > 220:
        voice_text = voice_text[:220] + "..."

    voice_id = VOICE_IDS.get(character, VOICE_IDS["Damian"])

    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json={
                "model_id": "eleven_monolingual_v1",
                "text": voice_text,
                "voice_settings": {
                    "stability": 0.85,
                    "similarity_boost": 0.75
                }
            },
            headers={
                "Accept": "audio/mpeg",
                "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
            }
        )
        response.raise_for_status()

        return Response(
            response.content,
            mimetype="audio/mpeg"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
